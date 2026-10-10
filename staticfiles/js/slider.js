class ReusableSlider {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;

        this.track = this.container.querySelector('.slider-track');
        this.prevBtn = this.container.querySelector('.slider-prev');
        this.nextBtn = this.container.querySelector('.slider-next');

        this.autoPlay = options.autoPlay || false;
        this.intervalTime = options.intervalTime || 4000;
        this.timer = null;

        this.init();
    }

    init() {
        if (!this.track) return;

        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.scroll('next');
            });
        }
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.scroll('prev');
            });
        }

        if (this.autoPlay) {
            this.startAutoPlay();

            // مدیریت ماوس در دسکتاپ
            this.container.addEventListener('mouseenter', () => this.stopAutoPlay());
            this.container.addEventListener('mouseleave', () => this.startAutoPlay());

            // مدیریت لمس در موبایل (شروع مجدد پس از برداشتن دست)
            this.container.addEventListener('touchstart', () => this.stopAutoPlay(), { passive: true });
            this.container.addEventListener('touchend', () => {
                // تاخیر کوتاه جهت اتمام حرکت لمسی
                setTimeout(() => this.startAutoPlay(), 2000);
            }, { passive: true });
        }
    }

    scroll(direction) {
        if (!this.track) return;
        const item = this.track.firstElementChild;
        if (!item) return;

        const style = window.getComputedStyle(this.track);
        const gap = parseInt(style.gap) || 0;
        const scrollAmount = item.offsetWidth + gap;

        const isRtl = document.dir === 'rtl' || document.documentElement.dir === 'rtl';
        let moveDistance = direction === 'next' ? scrollAmount : -scrollAmount;

        if (isRtl) {
            moveDistance = direction === 'next' ? -scrollAmount : scrollAmount;
        }

        this.track.scrollBy({
            left: moveDistance,
            behavior: 'smooth'
        });
    }

    startAutoPlay() {
        if (this.timer || !this.track) return;

        this.timer = setInterval(() => {
            const maxScroll = this.track.scrollWidth - this.track.clientWidth;
            const currentScroll = Math.abs(this.track.scrollLeft);

            // اگر به انتهای اسلایدر رسیدیم، به اسلاید اول برمی‌گردد
            if (currentScroll >= maxScroll - 20) {
                const isRtl = document.dir === 'rtl' || document.documentElement.dir === 'rtl';
                this.track.scrollTo({
                    left: 0,
                    behavior: 'smooth'
                });
            } else {
                this.scroll('next');
            }
        }, this.intervalTime);
    }

    stopAutoPlay() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }
}