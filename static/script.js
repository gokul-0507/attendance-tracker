function toggleDarkMode() {
  document.body.classList.toggle("bg-dark");
  document.body.classList.toggle("text-light");
  document.querySelectorAll(".card").forEach(c => c.classList.toggle("bg-secondary"));
}
