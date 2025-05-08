const smallScreen = document.querySelector(".small-screen");
const largeScreen = document.querySelector(".large-screen");
const buttons = document.querySelectorAll(".calc-btn");

let currentInput = "";
let previousInput = "";
let operation = null;
let resultDisplayed = false;

function updateDisplay() {
  smallScreen.textContent = previousInput + (operation ? " " + operation : "");
  largeScreen.textContent = currentInput || "0";
}

function clearAll() {
  currentInput = "";
  previousInput = "";
  operation = null;
  resultDisplayed = false;
  updateDisplay();
}

function appendNumber(num) {
  if (resultDisplayed) {
    currentInput = "";
    resultDisplayed = false;
  }

  if (num === "." && currentInput.includes(".")) return;
  currentInput += num;
  updateDisplay();
}

function chooseOperation(op) {
  if (!currentInput) return;
  if (previousInput) calculate();
  operation = op;
  previousInput = currentInput;
  currentInput = "";
  updateDisplay();
}

function calculate() {
  let result;
  const prev = parseFloat(previousInput);
  const curr = parseFloat(currentInput);
  if (isNaN(prev) || isNaN(curr)) return;

  switch (operation) {
    case "+":
      result = prev + curr;
      break;
    case "-":
      result = prev - curr;
      break;
    case "X":
      result = prev * curr;
      break;
    case "÷":
      result = prev / curr;
      break;
    default:
      return;
  }

  currentInput = result.toString();
  previousInput = "";
  operation = null;
  resultDisplayed = true;
  updateDisplay();
}

function toggleSign() {
  if (!currentInput) return;
  currentInput = (parseFloat(currentInput) * -1).toString();
  updateDisplay();
}

function percentage() {
  if (!currentInput) return;
  currentInput = (parseFloat(currentInput) / 100).toString();
  updateDisplay();
}

buttons.forEach((button) => {
  button.addEventListener("click", () => {
    const id = button.id;

    if (id.startsWith("num_")) {
      appendNumber(button.textContent);
    } else if (id === "dot") {
      appendNumber(".");
    } else if (id === "AC" || id === "clear") {
      clearAll();
    } else if (id === "plus") {
      chooseOperation("+");
    } else if (id === "minus") {
      chooseOperation("-");
    } else if (id === "multiply") {
      chooseOperation("X");
    } else if (id === "divide") {
      chooseOperation("÷");
    } else if (id === "equal") {
      calculate();
    } else if (id === "plus_minus") {
      toggleSign();
    } else if (id === "percent") {
      percentage();
    }
  });
});

updateDisplay();
