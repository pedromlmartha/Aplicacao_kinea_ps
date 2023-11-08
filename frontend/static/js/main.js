document.addEventListener('DOMContentLoaded', function() {
    // Quando o formulário for enviado, esta função será chamada
    document.getElementById('cotacao-form').addEventListener('submit', function(e) {
        e.preventDefault(); // Evita o envio do formulário de forma padrão

        var data = document.getElementById('data').value;
        if (data) {
            consultarCotacao(data);
        }
    });
});

function consultarCotacao() {
    var data = document.getElementById('data').value;
    fetch('http://127.0.0.1:5000/cotacao?data=' + data)
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            document.getElementById('resultado').textContent = 'Valor: ' + data.valor + ', Variação: ' + data.variacao + '%';
        })
        .catch(function(error) {
            console.error('Erro ao buscar cotação:', error);
            document.getElementById('resultado').textContent = 'Erro ao buscar cotação.';
        });
}
