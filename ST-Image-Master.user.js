// ==UserScript==
// @name         ST-Image-Master (SIM)
// @namespace    https://sillytavern.app/extensions
// @version      0.1.0
// @description  SillyTavern image generation enhancer with modular adapters and async queue.
// @author       SIM
// @match        *://*/*
// @grant        GM_xmlhttpRequest
// @connect      *
// ==/UserScript==

/* global GM_xmlhttpRequest, toastr, jQuery */

class SIMCore {
  constructor() {
    this.state = {
      queue: [],
      processing: false,
      logs: []
    };
    this.settingsKey = 'st_image_master';
    this.settings = this.loadSettings();
    this.ui = new SIMUI(this);
    this.parser = new SIMParser(this);
    this.connector = new SIMConnector(this);
  }

  init() {
    this.injectStyles();
    this.ui.render();
    this.ui.bindEvents();
    this.parser.startListening();
    this.log('SIM initialized.');
  }

  injectStyles() {
    const css = `
      #sim-panel {
        position: fixed;
        right: 24px;
        bottom: 24px;
        width: 360px;
        background: #e6e6e6;
        border-radius: 24px;
        box-shadow: 10px 10px 20px #c5c5c5, -10px -10px 20px #ffffff;
        padding: 16px;
        font-family: 'Segoe UI', sans-serif;
        z-index: 9999;
      }
      #sim-panel h3 { margin: 8px 0 12px; }
      #sim-panel input, #sim-panel textarea, #sim-panel select {
        width: 100%;
        border: none;
        border-radius: 12px;
        padding: 8px 10px;
        background: #e6e6e6;
        box-shadow: inset 5px 5px 10px #c5c5c5, inset -5px -5px 10px #ffffff;
        margin-bottom: 10px;
      }
      #sim-panel button {
        width: 100%;
        border: none;
        border-radius: 12px;
        padding: 10px;
        background: #e6e6e6;
        box-shadow: 5px 5px 10px #c5c5c5, -5px -5px 10px #ffffff;
        cursor: pointer;
      }
      #sim-preview {
        height: 160px;
        border-radius: 16px;
        background: #f2f2f2;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        margin-bottom: 10px;
      }
      #sim-preview img { max-width: 100%; max-height: 100%; }
      #sim-logs {
        height: 120px;
        overflow: auto;
        background: #ededed;
        border-radius: 12px;
        padding: 8px;
        font-size: 12px;
        box-shadow: inset 3px 3px 6px #c5c5c5, inset -3px -3px 6px #ffffff;
      }
    `;
    const style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
  }

  log(message) {
    const timestamp = new Date().toLocaleTimeString();
    this.state.logs.push(`[${timestamp}] ${message}`);
    this.ui.updateLogs();
  }

  enqueue(task) {
    this.state.queue.push(task);
    this.log(`Queued task: ${task.prompt}`);
    this.processQueue();
  }

  async processQueue() {
    if (this.state.processing) return;
    this.state.processing = true;
    while (this.state.queue.length) {
      const task = this.state.queue.shift();
      await this.connector.runTask(task);
    }
    this.state.processing = false;
  }

  loadSettings() {
    const base = this.getExtensionSettings();
    if (!base[this.settingsKey]) {
      base[this.settingsKey] = {
        apiType: 'custom',
        apiUrl: '',
        template: '{"prompt":"{{prompt}}","size":"{{size}}"}',
        path: 'data.img_url',
        size: '1024x1024',
        tags: ''
      };
    }
    return base[this.settingsKey];
  }

  saveSettings() {
    const base = this.getExtensionSettings();
    base[this.settingsKey] = this.settings;
    this.setExtensionSettings(base);
  }

  getExtensionSettings() {
    if (window.SillyTavern?.context?.extension_settings) {
      return window.SillyTavern.context.extension_settings;
    }
    window.SillyTavern = window.SillyTavern || { context: {} };
    window.SillyTavern.context.extension_settings = window.SillyTavern.context.extension_settings || {};
    return window.SillyTavern.context.extension_settings;
  }

  setExtensionSettings(settings) {
    if (window.SillyTavern?.context) {
      window.SillyTavern.context.extension_settings = settings;
    }
  }
}

class SIMParser {
  constructor(core) {
    this.core = core;
    this.tagRegex = /\[IMG_GEN\]([\s\S]*?)\[\/IMG_GEN\]/g;
  }

  startListening() {
    const eventSource = window.SillyTavern?.eventSource;
    if (eventSource?.on) {
      eventSource.on('message_updated', (message) => this.handleMessage(message));
    } else {
      this.core.log('Event source not found. Falling back to DOM observer.');
      this.observeDom();
    }
  }

  observeDom() {
    const container = document.body;
    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            this.scanNode(node);
          }
        });
      }
    });
    observer.observe(container, { childList: true, subtree: true });
  }

  scanNode(node) {
    const text = node.textContent || '';
    this.extractTags(text);
  }

  handleMessage(message) {
    const text = message?.message || message?.text || '';
    this.extractTags(text);
  }

  extractTags(text) {
    let match;
    while ((match = this.tagRegex.exec(text)) !== null) {
      const rawPrompt = match[1].trim();
      const fullPrompt = this.enrichPrompt(rawPrompt);
      this.core.enqueue({ prompt: fullPrompt, rawPrompt });
    }
  }

  enrichPrompt(prompt) {
    const description = this.getCharacterDescription();
    const tagExtras = this.core.settings.tags;
    return [prompt, description, tagExtras].filter(Boolean).join(', ');
  }

  getCharacterDescription() {
    const context = window.SillyTavern?.context;
    const char = context?.character || context?.characters?.[context?.characterId];
    return char?.description || '';
  }
}

class SIMConnector {
  constructor(core) {
    this.core = core;
    this.adapters = {
      comfyui: new SIMComfyUI(core),
      sdwebui: new SIMSDWebUI(core),
      custom: new SIMCustomAPI(core)
    };
  }

  async runTask(task) {
    const adapter = this.adapters[this.core.settings.apiType] || this.adapters.custom;
    try {
      const url = await adapter.generate(task);
      if (url) {
        this.core.ui.updatePreview(url);
        this.core.log('Image generated.');
      }
    } catch (error) {
      this.core.log(`Generation failed: ${error.message}`);
      toastr?.error?.(error.message || 'Generation failed');
    }
  }
}

class SIMBaseAdapter {
  constructor(core) {
    this.core = core;
  }

  gmFetch({ url, method = 'POST', data, headers = {} }) {
    return new Promise((resolve, reject) => {
      GM_xmlhttpRequest({
        url,
        method,
        headers,
        data: data ? JSON.stringify(data) : undefined,
        onload: (response) => {
          try {
            const json = JSON.parse(response.responseText);
            resolve(json);
          } catch (error) {
            reject(new Error('Invalid JSON response'));
          }
        },
        onerror: () => reject(new Error('Network error'))
      });
    });
  }

  async withRetry(fn) {
    let attempt = 0;
    let delay = 1000;
    while (attempt < 3) {
      try {
        return await fn(attempt + 1);
      } catch (error) {
        attempt += 1;
        if (attempt >= 3) throw error;
        this.core.log(`Retry ${attempt}/3 after error: ${error.message}`);
        this.core.ui.updateRetry(attempt);
        await new Promise((resolve) => setTimeout(resolve, delay));
        delay *= 2;
      }
    }
    return null;
  }
}

class SIMCustomAPI extends SIMBaseAdapter {
  buildPayload(task) {
    const template = this.core.settings.template || '{}';
    return this.applyTemplate(template, {
      prompt: task.prompt,
      size: this.core.settings.size
    });
  }

  applyTemplate(template, params) {
    const output = Object.keys(params).reduce((acc, key) => {
      const value = params[key];
      return acc.replaceAll(`{{${key}}}`, String(value));
    }, template);
    try {
      return JSON.parse(output);
    } catch (error) {
      throw new Error('Template JSON invalid');
    }
  }

  sniffPath(obj, path) {
    return path.split('.').reduce((acc, key) => (acc ? acc[key] : undefined), obj);
  }

  async generate(task) {
    const payload = this.buildPayload(task);
    return this.withRetry(async (attempt) => {
      this.core.log(`Custom API request (attempt ${attempt})`);
      const data = await this.gmFetch({
        url: this.core.settings.apiUrl,
        data: payload
      });
      const url = this.sniffPath(data, this.core.settings.path);
      if (!url) throw new Error('Image URL not found');
      return url;
    });
  }
}

class SIMComfyUI extends SIMBaseAdapter {
  async generate(task) {
    return this.withRetry(async (attempt) => {
      this.core.log(`ComfyUI request (attempt ${attempt})`);
      const payload = { prompt: task.prompt };
      const data = await this.gmFetch({ url: this.core.settings.apiUrl, data: payload });
      return data?.images?.[0]?.url || '';
    });
  }
}

class SIMSDWebUI extends SIMBaseAdapter {
  async generate(task) {
    return this.withRetry(async (attempt) => {
      this.core.log(`SDWebUI request (attempt ${attempt})`);
      const payload = {
        prompt: task.prompt,
        width: 1024,
        height: 1024
      };
      const data = await this.gmFetch({ url: this.core.settings.apiUrl, data: payload });
      return data?.images?.[0] || '';
    });
  }
}

class SIMUI {
  constructor(core) {
    this.core = core;
    this.$panel = null;
  }

  render() {
    const $ = jQuery;
    this.$panel = $(
      `<div id="sim-panel">
        <h3>ST-Image-Master</h3>
        <label>API Type</label>
        <select id="sim-api-type">
          <option value="custom">Custom API</option>
          <option value="comfyui">ComfyUI</option>
          <option value="sdwebui">SDWebUI</option>
        </select>
        <label>API URL</label>
        <input id="sim-api-url" type="text" placeholder="https://api.example.com/generate" />
        <label>Template (Custom API)</label>
        <textarea id="sim-template" rows="3"></textarea>
        <label>Path Sniffing</label>
        <input id="sim-path" type="text" placeholder="data.img_url" />
        <label>Size</label>
        <input id="sim-size" type="text" placeholder="1024x1024" />
        <label>Tag Editor</label>
        <textarea id="sim-tags" rows="2"></textarea>
        <div id="sim-preview">Preview</div>
        <button id="sim-save">Save Settings</button>
        <h4>Runtime Logs</h4>
        <div id="sim-logs"></div>
        <div id="sim-retry"></div>
      </div>`
    );
    $('body').append(this.$panel);
    this.fillSettings();
  }

  bindEvents() {
    const $ = jQuery;
    $('#sim-save').on('click', () => {
      this.core.settings.apiType = $('#sim-api-type').val();
      this.core.settings.apiUrl = $('#sim-api-url').val();
      this.core.settings.template = $('#sim-template').val();
      this.core.settings.path = $('#sim-path').val();
      this.core.settings.size = $('#sim-size').val();
      this.core.settings.tags = $('#sim-tags').val();
      this.core.saveSettings();
      toastr?.success?.('SIM settings saved');
    });
  }

  fillSettings() {
    const settings = this.core.settings;
    jQuery('#sim-api-type').val(settings.apiType);
    jQuery('#sim-api-url').val(settings.apiUrl);
    jQuery('#sim-template').val(settings.template);
    jQuery('#sim-path').val(settings.path);
    jQuery('#sim-size').val(settings.size);
    jQuery('#sim-tags').val(settings.tags);
  }

  updatePreview(url) {
    const preview = this.$panel.find('#sim-preview');
    preview.empty();
    preview.append(`<img src="${url}" alt="preview" />`);
  }

  updateLogs() {
    const logBox = this.$panel.find('#sim-logs');
    logBox.text(this.core.state.logs.slice(-50).join('\n'));
  }

  updateRetry(attempt) {
    this.$panel.find('#sim-retry').text(`Retry attempt: ${attempt}`);
  }
}

(function initSIM() {
  const start = () => {
    if (!window.jQuery || !window.toastr) {
      setTimeout(start, 1000);
      return;
    }
    const core = new SIMCore();
    core.init();
  };
  start();
})();
