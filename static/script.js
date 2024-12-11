document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("prediction-form");
  const resultText = document.getElementById("result-text");
  const resultModal = document.getElementById("resultModal");
  const closeButton = document.querySelector(".btn-close");

  // Đóng modal
  closeButton.addEventListener("click", () => {
      resultModal.style.display = "none";
  });

  // Ngăn form reload và gửi dữ liệu qua AJAX
  form.addEventListener("submit", async function (event) {
      event.preventDefault(); // Ngăn việc gửi form thông thường

      // Thu thập dữ liệu từ form
      const formData = new FormData(form);

      try {
          // Gửi dữ liệu đến server qua fetch API
          const response = await fetch("/predict", {
              method: "POST",
              body: formData
          });

          if (response.ok) {
              const data = await response.json(); // Nhận kết quả JSON từ server
              resultText.textContent = data.result; // Gắn kết quả vào modal
              resultModal.style.display = "block"; // Hiển thị modal
          } else {
              resultText.textContent = "Đã xảy ra lỗi. Vui lòng thử lại.";
              resultModal.style.display = "block";
          }
      } catch (error) {
          resultText.textContent = "Không thể kết nối đến server. Vui lòng thử lại.";
          resultModal.style.display = "block";
      }
  });
});
