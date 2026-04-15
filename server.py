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
    { id: 'p2', codigo: 'PP 0104', titulo: 'Reducción de la Mortalidad por Emergencias y Urgencias', hoja: 'PP 0104' },
    { id: 'p3', codigo: 'PP 0131', titulo: 'Control y Prevención en Salud Mental', hoja: 'PP 0131' },
    { id: 'p4', codigo: 'PP 0018', titulo: 'Enfermedades No Transmisibles', hoja: 'PP 0018' },
    { id: 'p5', codigo: 'PP 0024', titulo: 'Prevención y Control del Cáncer', hoja: 'PP 0024' },
    { id: 'p6', codigo: 'PP 0068', titulo: 'Reducción de Vulnerabilidad y Atención de Emergencias', hoja: 'PP 0068' },
  ];

  var ESCENARIOS = {
    'PP 0001': { factor: 0.85, label: 'alta' },
    'PP 0104': { factor: 0.62, label: 'media' },
    'PP 0131': { factor: 0.38, label: 'baja' },
    'PP 0018': { factor: 0.91, label: 'alta' },
    'PP 0024': { factor: 0.55, label: 'media' },
    'PP 0068': { factor: 0.28, label: 'baja' },
  };

  function mockDatos(hojaName) {
    var titulo = '';
    MOCK_PROGRAMAS.forEach(function(p){ if(p.hoja===hojaName) titulo = p.titulo; });
    var esc = ESCENARIOS[hojaName] || { factor: 0.6 };
    var f   = esc.factor;
    var metas = [
      {
        producto: '3000001 - Acciones comunes',
        codigoProducto: '3000001',
        subProducto: 'Sub 01',
        actividad: 'Actividad de atención directa',
        unidadMedida: 'Persona',
        metaReprog: 1200,
        metaProg: 1200,
        meses: [Math.round(100*f),Math.round(100*f),Math.round(100*f),Math.round(100*f),
                Math.round(100*f),Math.round(100*f),Math.round(100*f),0,0,0,0,0],
        totalMeta: Math.round(1200*f*0.58),
        avancePct: Math.round(f*85*100)/100,
      },
      {
        producto: '3000001 - Acciones comunes',
        codigoProducto: '3000001',
        subProducto: 'Sub 02',
        actividad: 'Seguimiento y monitoreo',
        unidadMedida: 'Atención',
        metaReprog: 800,
        metaProg: 800,
        meses: [Math.round(70*f),Math.round(70*f),Math.round(70*f),Math.round(70*f),
                Math.round(70*f),Math.round(70*f),Math.round(50*f),0,0,0,0,0],
        totalMeta: Math.round(800*f*0.56),
        avancePct: Math.round(f*80*100)/100,
      },
      {
        producto: '3000694 - Gestión de la calidad',
        codigoProducto: '3000694',
        subProducto: '',
        actividad: 'Control y mejora continua',
        unidadMedida: 'Documento',
        metaReprog: 24,
        metaProg: 24,
        meses: [Math.round(2*f),Math.round(2*f),Math.round(2*f),Math.round(2*f),
                Math.round(2*f),Math.round(2*f),Math.round(2*f),0,0,0,0,0],
        totalMeta: Math.round(24*f*0.6),
        avancePct: Math.round(f*80*100)/100,
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

  function makeRunner(){
    var _success = function(){};
    var _failure = function(){};
    var runner = {
      withSuccessHandler: function(fn){ _success = fn; return runner; },
      withFailureHandler: function(fn){ _failure = fn; return runner; },
      getProgramas: function(){
        var cb = _success;
        setTimeout(function(){ cb(MOCK_PROGRAMAS); }, 200);
      },
      getDatosHoja: function(hojaName){
        var cb = _success;
        var delay = 200 + Math.random()*300;
        setTimeout(function(){ cb(mockDatos(hojaName)); }, delay);
      },
    };
    return runner;
  }

  window.google = {
    script: {
      get run(){ return makeRunner(); }
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
