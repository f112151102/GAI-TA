// 傳送訊息到 Flask 後端
function sendMessage() {
  const input = document.getElementById("message");
  const chatbox = document.getElementById("chatbox");
  const userText = input.value.trim();

  if (userText === "") return;

  // 顯示使用者訊息
  chatbox.innerHTML += `<p><strong>你：</strong> ${userText}</p>`;
  input.value = "";

  // 顯示等待回覆提示
  chatbox.innerHTML += `<p id="loading">🤖 GPT 思考中...</p>`;
  chatbox.scrollTop = chatbox.scrollHeight;

  // 傳送 POST 請求到 Flask /chat API
  fetch("/chat_api", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userText })
  })
  .then(res => res.json())
  .then(data => {
    // 移除 loading 提示
    document.getElementById("loading").remove();

    // 顯示 GPT 回覆
    chatbox.innerHTML += `<p><strong>GPT：</strong> ${data.reply}</p>`;
    chatbox.scrollTop = chatbox.scrollHeight;
  })
  .catch(error => {
    document.getElementById("loading").remove();
    chatbox.innerHTML += `<p style="color:red;">❗ 錯誤：無法取得 GPT 回覆</p>`;
  });
}

// 加入 Enter 快捷鍵送出訊息
document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("message").addEventListener("keydown", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  });
});
