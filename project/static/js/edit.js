"use strict";

function enterToBr(event) {
  console.log("raise event");
  if (event.code === "Enter") {
    console.log("key down enter");
    event.preventDefault();
    //     text = document.getElementById("content");
    //     text.replaceAll("\n", "<br/>");
    //   }
  }
}

window.onload = enterToBr;
