function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function printComDelay(texto, elemento, delayMs = 50) {
  elemento.textContent = ""; // limpa o elemento

  for (const ch of texto) {
    await sleep(delayMs);
    elemento.textContent += ch; // escreve letra por letra no elemento
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const saida = document.getElementById("saida");
  const botao = document.getElementById("btnDigitar");

  botao.addEventListener("click", () => {
    printComDelay("Fala deleeee!", saida, 50);
  });
});