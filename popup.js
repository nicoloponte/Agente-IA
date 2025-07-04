document.getElementById("sendButton").addEventListener("click", function () {
    const command = document.getElementById("commandInput").value;
    fetch("http://localhost:5000/api/agent", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ command: command }),
    })
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("responseArea").textContent = data.response;
      });
  });