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
            var resultado = 'Valor: ' + data.valor + ', Variação: ' + data.variacao + '%';
            var variacaoAbs = Math.abs(data.variacao);

            if (variacaoAbs >= -0.93 && variacaoAbs <= 0.93) {
                resultado += ' - Variação Bastante Relevante';
            } else if (variacaoAbs >= -1.85 && variacaoAbs <= 1.85) {
                resultado += ' - Variação Relevante';
            } else if (variacaoAbs >= -2.78 && variacaoAbs <= 2.78) {
                resultado += ' - Variação Pouco Relevante';
            } else {
                resultado += ' - Variação Irrelevante';
            }

            document.getElementById('resultado').textContent = resultado;
        })
        .catch(function(error) {
            console.error('Erro ao buscar cotação:', error);
            document.getElementById('resultado').textContent = 'Erro ao buscar cotação.';
        });
}
