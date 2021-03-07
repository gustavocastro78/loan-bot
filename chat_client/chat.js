const botChannel = {
  address: "http://localhost:5005/webhooks/rest/webhook",
  connector: null,
  setup: () => {},
  sendMessage: (message) => {
    fetch(botChannel.address, {
      body: JSON.stringify(message),
      method: "POST",
      mode: "cors",
      credentials: "same-origin",
      referrer: "about:client",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    })
      .then((e) => e.json())
      .then((data) => {
        document.dispatchEvent(
          new CustomEvent("message_received", { detail: data })
        );
      });
  },
};

const chatChannel = {
  address: "",
  connector: null,
  setup: (senderType) => {
    chatChannel.connector = new WebSocket(`ws://${chatChannel.address}`);

    chatChannel.connector.onopen = () => {
      chatChannel.sendMessage({ action: `new_${senderType}` });
    };

    chatChannel.connector.onmessage = (e) => {
      document.dispatchEvent(
        new CustomEvent("message_received", { detail: [JSON.parse(e.data)] })
      );
    };
  },
  sendMessage: (message) => {
    chatChannel.connector.send(JSON.stringify(message));
  },
};

/**
 *
 * @param {string} senderType
 * @returns {string}
 */
const generateSenderId = (senderType = "client") => {
  return `${new Date().getTime()}_${senderType}`;
};

const messageMenager = {
  channel: botChannel,
  senderType: document.getElementById("sender-type").value,
  senderId: generateSenderId(this.senderType),
};

/**
 *
 * @param {string} sender
 * @param {string} message
 * @returns {object}
 */
const buildMessage = (sender, message) => {
  return {
    sender: sender,
    action: "new_message",
    message: message,
  };
};

/**
 *
 * @param {object} message
 * @returns {HTMLElementTagNameMap}
 */
const createTextElement = (message) => {
  const messageElement = document.createElement("span");
  const text = message.text ?? message.message;
  messageElement.innerHTML = text.replace(/\n/g, "<br />");

  return messageElement;
};

/**
 *
 * @param {object} message
 * @returns {HTMLElementTagNameMap}
 */
const createImageElement = (message) => {
  const imageElement = document.createElement("img");
  imageElement.src = message.image;
  imageElement.width = 250;

  return imageElement;
};

/**
 *
 * @param {object} messages
 * @param {string} className
 */
const plotMessage = (message = {}, className = "message-to") => {
  const messageElement = message.image
    ? createImageElement(message)
    : createTextElement(message);

  const element = document.createElement("div");
  element.className = className;
  element.appendChild(messageElement);

  document.getElementById("dialog-area").appendChild(element);
};

const manageMessages = (messages = [{}]) => {
  messages.map((message) => {
    switch (true) {
      case message.custom !== undefined:
        messageMenager.channel = chatChannel;
        messageMenager.channel.address = message.custom.host;
        messageMenager.channel.setup(messageMenager.senderType);
        break;
      case message.text !== undefined:
      case message.image !== undefined:
        plotMessage(message, "message-to");
        break;
    }
  });
};

document.addEventListener("message_received", (e) => {
  manageMessages(e.detail);
});

const sendMessage = () => {
  const textArea = document.getElementById("text-area");

  if (textArea.textContent.trim() == '') {
    return
  }

  const msg = buildMessage(
    messageMenager.senderType,
    textArea.textContent.trim()
  );
  textArea.textContent = "";

  plotMessage(msg, "message-from");

  messageMenager.channel.sendMessage(msg);
};
