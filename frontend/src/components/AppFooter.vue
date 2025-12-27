<template>
  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-left">
        <div class="brand">Learning Centers</div>
        <div class="copy">© {{ year }} Learning Centers. Все права защищены.</div>
      </div>

      <div class="footer-contacts">
        <div class="contact-title">
          Хотите добавить свои образовательные программы в нашу систему?
        </div>

        <div class="contact-text">
          Свяжитесь с нами, и мы подключим ваш учебный центр.
        </div>

        <div class="contact-items">
          <a class="contact-link" href="mailto:info@learning-centers.kg">
            📧 info@learning-centers.kg
          </a>

          <a class="contact-link" href="tel:+996999223135">
            📞 +996 999223135
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
</script>

<style scoped>
.site-footer {
  margin-top: auto;
  border-top: 1px solid rgba(148,163,184,.25);
  background: rgba(15,23,42,.9);
  backdrop-filter: blur(10px);
}

.footer-inner {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 24px;
  padding: 22px 0;
  color: #e2e8f0;
}

.footer-left {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.brand {
  font-weight: 800;
  font-size: 18px;
  letter-spacing: .02em;
}

.copy {
  font-size: 13px;
  opacity: .7;
}

.footer-contacts {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.contact-title {
  font-weight: 700;
  font-size: 15px;
}

.contact-text {
  font-size: 14px;
  opacity: .85;
}

.contact-items {
  display: flex;
  gap: 18px;
  margin-top: 6px;
  flex-wrap: wrap;
}

.contact-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #e2e8f0;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  padding: 6px 10px;
  border-radius: 10px;
  border: 1px solid rgba(148,163,184,.35);
  background: rgba(148,163,184,.08);
}

.contact-link:hover {
  background: rgba(148,163,184,.18);
}

@media (max-width: 820px) {
  .footer-inner {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}
</style>
