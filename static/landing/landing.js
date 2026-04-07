(() => {
    const navbar = document.querySelector('.navbar');
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const prevButton = document.getElementById('prevDev');
    const nextButton = document.getElementById('nextDev');
    const indicators = document.querySelectorAll('.indicator');
    const totalSlides = 4;
    let currentSlide = 1;

    function toggleMobileMenu(forceClose = false) {
        if (!mobileMenuBtn || !mobileMenu) {
            return;
        }

        const shouldOpen = forceClose ? false : !mobileMenuBtn.classList.contains('active');
        mobileMenuBtn.classList.toggle('active', shouldOpen);
        mobileMenu.classList.toggle('active', shouldOpen);
        document.body.classList.toggle('menu-open', shouldOpen);
    }

    function showSlide(requestedSlide) {
        const cards = document.querySelectorAll('.developer-card');
        if (!cards.length) {
            return;
        }

        if (requestedSlide > totalSlides) {
            currentSlide = 1;
        } else if (requestedSlide < 1) {
            currentSlide = totalSlides;
        } else {
            currentSlide = requestedSlide;
        }

        cards.forEach((card) => card.classList.remove('active'));
        indicators.forEach((dot) => dot.classList.remove('active'));

        const activeCard = document.querySelector(`.developer-card[data-dev="${currentSlide}"]`);
        const activeIndicator = document.querySelector(`.indicator[data-slide="${currentSlide}"]`);

        if (activeCard) {
            activeCard.classList.add('active');
        }

        if (activeIndicator) {
            activeIndicator.classList.add('active');
        }
    }

    function setupSmoothAnchors() {
        document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
            anchor.addEventListener('click', (event) => {
                const href = anchor.getAttribute('href');
                if (!href || href === '#') {
                    return;
                }

                const target = document.querySelector(href);
                if (!target) {
                    return;
                }

                event.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                toggleMobileMenu(true);
            });
        });
    }

    function setupNavbarScrollState() {
        if (!navbar) {
            return;
        }

        const setState = () => {
            navbar.classList.toggle('scrolled', window.scrollY > 16);
        };

        setState();
        window.addEventListener('scroll', setState, { passive: true });
    }

    function setupRevealAnimation() {
        const sections = document.querySelectorAll('.about, .features, .modules, .credits, .cta, .hero-metrics');
        if (!sections.length || !('IntersectionObserver' in window)) {
            return;
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.22
        });

        sections.forEach((section) => {
            section.classList.add('reveal');
            observer.observe(section);
        });
    }

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => toggleMobileMenu(false));
    }

    document.querySelectorAll('.mobile-link, .mobile-link-btn').forEach((link) => {
        link.addEventListener('click', () => toggleMobileMenu(true));
    });

    if (prevButton) {
        prevButton.addEventListener('click', () => showSlide(currentSlide - 1));
    }

    if (nextButton) {
        nextButton.addEventListener('click', () => showSlide(currentSlide + 1));
    }

    indicators.forEach((indicator) => {
        indicator.addEventListener('click', () => {
            const slide = Number(indicator.getAttribute('data-slide'));
            if (Number.isFinite(slide)) {
                showSlide(slide);
            }
        });
    });

    setupSmoothAnchors();
    setupNavbarScrollState();
    setupRevealAnimation();
})();
