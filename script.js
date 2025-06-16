const form = document.getElementById("form");
const respostaDiv = document.getElementById("resposta");
const listaDiv = document.getElementById("lista");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const cpf = document.getElementById("cpf").value;
    const nome = document.getElementById("nome").value;
    const nascimento = document.getElementById("nascimento").value;
    const cep = document.getElementById("cep").value;

    const paciente = { cpf, nome, nascimento, cep };

    try {
        const res = await fetch("http://127.0.0.1:5000/paciente", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(paciente),
        });

        const data = await res.json();
        respostaDiv.textContent = JSON.stringify(data, null, 2);
        form.reset();
    } catch (err) {
        respostaDiv.textContent = "Erro ao cadastrar: " + err;
    }
});

async function listarPacientes() {
    try {
        const res = await fetch("http://127.0.0.1:5000/pacientes");
        const pacientes = await res.json();

        listaDiv.innerHTML = "<h2>Pacientes</h2><ul>" + pacientes.map((p) => `<li><strong>${p.nome}</strong> - CPF: ${p.cpf} - Nasc: ${p.nascimento} - CEP: ${p.cep}</li>`).join("") + "</ul>";
    } catch (err) {
        listaDiv.textContent = "Erro ao listar pacientes: " + err;
    }
}
