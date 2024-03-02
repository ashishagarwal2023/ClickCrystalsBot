let code;
      function toggleUsageVisibility() {
        const usageDiv = document.getElementById("usage");
        const messageDivs = document.querySelectorAll("#chat .message");

        if (messageDivs.length === 0) {
          usageDiv.style.display = "block";
        } else {
          usageDiv.style.display = "none";
        }
      }

      const chatMain = document.getElementById("chat");
      const observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
          mutation.addedNodes.forEach(function (node) {
            if (node.classList && node.classList.contains("message")) {
              toggleUsageVisibility();
            }
          });
        });
      });

      const observerConfig = {
        childList: true,
        subtree: true,
      };

      observer.observe(chatMain, observerConfig);

    // clear button
const clearButton = document.getElementById("clear");
clearButton.addEventListener("click", function () {
  // Send request to reset chat session
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/new_chat", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.onreadystatechange = function () {
    if (xhr.readyState == XMLHttpRequest.DONE) {
      if (xhr.status == 200) {
        console.log("Chat session reset successfully");
        // After successful reset, remove all messages
        const messageDivs = document.querySelectorAll("#chat .message");
        messageDivs.forEach(function (messageDiv) {
          messageDiv.remove();
        });
        toggleUsageVisibility();
      } else {
        console.error("Failed to reset chat session:", xhr.statusText);
      }
    }
  };
  xhr.send();
});

      function sendMessage() {
        var userInput =
          document.getElementById("userInput").value.trim() === ""
            ? "(no prompt)"
            : document.getElementById("userInput").value.trim();
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/get_response", true);
        xhr.setRequestHeader(
          "Content-Type",
          "application/x-www-form-urlencoded"
        );
        console.log("Sending message")
        xhr.onreadystatechange = function () {
          if (xhr.readyState == XMLHttpRequest.DONE) {
            if (xhr.status == 200) {
              var resp = marked.parse(xhr.responseText);
              console.log("Response fetched successfully.");
              document.getElementById(
                "chat"
              ).innerHTML += `<div class="message">
                    <div class="user">${userInput}</div>
                    <div class="assistant">
                        <p><span>${resp}</span></p>
                    </div>
                </div>`;
            } else {
              var errorUrl = "/get_response";
              var errorCode = xhr.status;
              var errorMessage =
                "Error: POST <a href='" +
                errorUrl +
                "'>" +
                errorUrl +
                "</a> " +
                errorCode;
              console.error(`Error: POST ${errorUrl} ${errorCode} - ${xhr.statusText}`);
              document.getElementById(
                "chat"
              ).innerHTML += `<div class="message">
                    <div class="user">${userInput}</div>
                    <div class="assistant">
                        <p><span class="error">${errorMessage}</span></p>
                    </div>
                </div>`;
                console.log("Failed to send message or recieve response");
            }
          }
        };
        xhr.send("user_input=" + userInput);
      }

      document.getElementById("submitBtn").onclick = function () {
        sendMessage();
        document.getElementById("userInput").value = "";
      };