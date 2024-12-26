document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("prediction-form");
  const resultText = document.getElementById("result-text");
  const resultModal = document.getElementById("resultModal");
  const closeButton = document.querySelector(".btn-close");

  closeButton.addEventListener("click", () => {
      resultModal.style.display = "none";
  });

  form.addEventListener("submit", async function (event) {
      event.preventDefault(); // Ngăn gửi form

      const formData = new FormData(form);

      try {
          const response = await fetch("/predict", {
              method: "POST",
              body: formData
          });

          if (response.ok) {
              const data = await response.json(); 
              resultText.textContent = data.result; 
              resultModal.style.display = "block";
          } else {
              resultText.textContent = "Đã xảy ra lỗi!";
              resultModal.style.display = "block";
          }
      } catch (error) {
          resultText.textContent = "Không thể kết nối đến server.";
          resultModal.style.display = "block";
      }
  });
});
