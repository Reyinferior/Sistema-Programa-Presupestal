#!/usr/bin/env python3
"""Simple HTTP server that serves sistema_ppr.html with a google.script mock injected."""

import http.server
import socketserver
import os

PORT = 5000
HOST = "0.0.0.0"

MOCK_SCRIPT = """
<script>
// ── Mock google.script.run for Replit preview ──────────────────
(function(){
  var MOCK_PROGRAMAS = [
    { id: 'p1', codigo: 'PP 0001', titulo: 'Programa Articulado Nutricional', hoja: 'PP 0001' },
    { id: 'p2', codigo: 'PP 0104', titulo: 'Reducción de la Mortalidad por Emergencias', hoja: 'PP 0104' },
    { id: 'p3', codigo: 'PP 0131', titulo: 'Control y Prevención en Salud Mental', hoja: 'PP 0131' },
  ];

  function mockDatos(hojaName) {
    var titulo = '';
    MOCK_PROGRAMAS.forEach(function(p){ if(p.hoja===hojaName) titulo = p.titulo; });
    var metas = [
      {
        producto: '3000001 - Acciones comunes',
        codigoProducto: '3000001',
        subProducto: 'Sub 01',
        actividad: 'Actividad de demostración',
        unidadMedida: 'Persona',
        metaReprog: 1200,
        metaProg: 1200,
        meses: [100,100,100,100,100,100,100,50,0,0,0,0],
        totalMeta: 750,
        avancePct: 62.5,
      },
      {
        producto: '3000001 - Acciones comunes',
        codigoProducto: '3000001',
        subProducto: 'Sub 02',
        actividad: 'Segunda actividad',
        unidadMedida: 'Atención',
        metaReprog: 800,
        metaProg: 800,
        meses: [70,70,70,70,70,70,50,0,0,0,0,0],
        totalMeta: 470,
        avancePct: 58.75,
      },
      {
        producto: '3000694 - Gestión de la calidad',
        codigoProducto: '3000694',
        subProducto: '',
        actividad: 'Control de calidad',
        unidadMedida: 'Documento',
        metaReprog: 24,
        metaProg: 24,
        meses: [2,2,2,2,2,2,2,0,0,0,0,0],
        totalMeta: 14,
        avancePct: 58.33,
      },
    ];
    var totMetaProg = 0, totTotal = 0, totMeses = [0,0,0,0,0,0,0,0,0,0,0,0];
    metas.forEach(function(m){
      totMetaProg += m.metaProg;
      totTotal    += m.totalMeta;
      m.meses.forEach(function(v,i){ totMeses[i] += v; });
    });
    return {
      titulo: titulo || hojaName,
      hoja: hojaName,
      metas: metas,
      totales: {
        metaReprog: totMetaProg,
        metaProg: totMetaProg,
        meses: totMeses,
        totalMeta: totTotal,
        avancePct: Math.round((totTotal/totMetaProg)*10000)/100,
      }
    };
  }

  window.google = {
    script: {
      run: (function(){
        var _success = function(){};
        var _failure = function(){};
        var obj = {
          withSuccessHandler: function(fn){ _success = fn; return obj; },
          withFailureHandler: function(fn){ _failure = fn; return obj; },
          getProgramas: function(){
            setTimeout(function(){ _success(MOCK_PROGRAMAS); }, 200);
          },
          getDatosHoja: function(hojaName){
            setTimeout(function(){ _success(mockDatos(hojaName)); }, 300);
          },
        };
        return obj;
      })(),
    }
  };
})();
</script>
"""

HTML_FILE = os.path.join(os.path.dirname(__file__), "sistema_ppr.html")


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            try:
                with open(HTML_FILE, "r", encoding="utf-8") as f:
                    content = f.read()
                # Inject mock before </head>
                content = content.replace("</head>", MOCK_SCRIPT + "\n</head>", 1)
                encoded = content.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)
            except Exception as e:
                self.send_error(500, str(e))
        else:
            super().do_GET()

    def log_message(self, fmt, *args):
        print(f"[server] {fmt % args}")


if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
        print(f"Serving on http://{HOST}:{PORT}")
        httpd.serve_forever()
