/**
 * device.js — Shared device detection and viewport adaptation utility.
 * Used by both the landing page and the internal PWA app.
 *
 * Detects: device type (mobile/tablet/desktop), orientation, touch capability,
 * viewport width, and connection quality. Exposes window.DeviceInfo.
 *
 * Emits a 'device:change' event when viewport category changes.
 */
(function () {
  const DeviceInfo = {
    type: 'desktop',        // 'mobile' | 'tablet' | 'desktop'
    orientation: 'landscape', // 'portrait' | 'landscape'
    isTouch: false,
    isMobile: false,
    isTablet: false,
    isDesktop: false,
    viewportWidth: 0,
    viewportHeight: 0,
    connectionType: 'unknown',
    saveData: false,
    dpr: 1,                 // device pixel ratio

    /**
     * Detect device type from viewport width and user agent.
     */
    detect() {
      this.viewportWidth = window.innerWidth;
      this.viewportHeight = window.innerHeight;
      this.dpr = window.devicePixelRatio || 1;
      this.orientation = this.viewportHeight > this.viewportWidth ? 'portrait' : 'landscape';

      // Touch detection
      this.isTouch = window.matchMedia('(pointer: coarse)').matches ||
        ('ontouchstart' in window && navigator.maxTouchPoints > 0);

      // User agent hints
      const ua = navigator.userAgent || '';
      const uaMobile = /Android|iPhone|iPod|Windows Phone/i.test(ua);
      const uaTablet = /iPad|Android.*Tablet|Silk|PlayBook/i.test(ua) ||
        (/Android/i.test(ua) && !/Mobile/i.test(ua));

      // Viewport-based classification (primary)
      if (this.viewportWidth < 768) {
        this.type = 'mobile';
      } else if (this.viewportWidth < 1024) {
        this.type = 'tablet';
      } else {
        this.type = 'desktop';
      }

      // UA override: force mobile if UA says mobile and viewport is small
      if (uaMobile && this.viewportWidth < 900) {
        this.type = 'mobile';
      }

      this.isMobile = this.type === 'mobile';
      this.isTablet = this.type === 'tablet';
      this.isDesktop = this.type === 'desktop';

      // Connection info
      if (navigator.connection) {
        this.connectionType = navigator.connection.effectiveType || 'unknown';
        this.saveData = navigator.connection.saveData || false;
      }

      // Apply data attributes to <html> for CSS targeting
      const html = document.documentElement;
      html.setAttribute('data-device', this.type);
      html.setAttribute('data-orientation', this.orientation);
      html.setAttribute('data-touch', String(this.isTouch));

      // Save to localStorage
      localStorage.setItem('device_type', this.type);
      localStorage.setItem('device_orientation', this.orientation);
      localStorage.setItem('device_touch', String(this.isTouch));

      return this.getReport();
    },

    /**
     * Start listening for viewport changes and emit events.
     */
    watch() {
      let resizeTimer = null;
      let prevType = this.type;

      const handler = () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
          const oldType = prevType;
          this.detect();
          if (this.type !== oldType) {
            prevType = this.type;
            window.dispatchEvent(new CustomEvent('device:change', {
              detail: this.getReport()
            }));
            console.log('[Device] Type changed:', oldType, '→', this.type);
          }
        }, 150);
      };

      window.addEventListener('resize', handler);
      window.addEventListener('orientationchange', handler);

      // Also use matchMedia for precise breakpoint tracking
      const mobileMQ = window.matchMedia('(max-width: 767px)');
      const tabletMQ = window.matchMedia('(min-width: 768px) and (max-width: 1023px)');
      try {
        mobileMQ.addEventListener('change', handler);
        tabletMQ.addEventListener('change', handler);
      } catch (e) {
        // Safari < 14 fallback
        mobileMQ.addListener(handler);
        tabletMQ.addListener(handler);
      }
    },

    /**
     * Get a summary report.
     */
    getReport() {
      return {
        type: this.type,
        orientation: this.orientation,
        isTouch: this.isTouch,
        isMobile: this.isMobile,
        isTablet: this.isTablet,
        isDesktop: this.isDesktop,
        viewportWidth: this.viewportWidth,
        viewportHeight: this.viewportHeight,
        dpr: this.dpr,
        connectionType: this.connectionType,
        saveData: this.saveData,
        summary: `${this.type} · ${this.orientation} · ${this.viewportWidth}×${this.viewportHeight} · touch:${this.isTouch}`
      };
    }
  };

  // Auto-detect on load
  DeviceInfo.detect();
  DeviceInfo.watch();

  // Expose globally
  window.DeviceInfo = DeviceInfo;
  console.log('[Device]', DeviceInfo.getReport().summary);
})();