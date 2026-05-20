import '../styles/contacto.css'

function Contacto() {
  return (
    <div className="contact-page">

      <section className="contact-hero">
        <div className="container">

          <span className="contact-badge">
            Zeezton Store
          </span>

          <h1 className="contact-title">
            Hablemos de tu próximo proyecto
          </h1>

          <p className="contact-text">
            Contáctanos para cotizaciones, asesorías, repuestos,
            desarrollo web o soluciones digitales personalizadas.
          </p>

        </div>
      </section>

      <section className="contact-section">
        <div className="container">

          <div className="contact-grid">

            <div className="contact-info-box">

              <h2>Información</h2>

              <p>
                Estamos disponibles para ayudarte con proyectos,
                cotizaciones y soluciones digitales modernas.
              </p>

              <div className="contact-info-item">
                <span>📧</span>
                <div>
                  <strong>Email</strong>
                  <p>millwords.solutions@gmail.com</p>
                </div>
              </div>

              <div className="contact-info-item">
                <span>📱</span>
                <div>
                  <strong>WhatsApp</strong>
                  <p>+56 9 6433 3347</p>
                </div>
              </div>

              <div className="contact-info-item">
                <span>🌐</span>
                <div>
                  <strong>Sitio Web</strong>
                  <p>www.zeezton.cl</p>
                </div>
              </div>

            </div>

            <form className="contact-form">

              <div className="form-group">
                <label>Nombre</label>
                <input
                  type="text"
                  placeholder="Ingresa tu nombre"
                />
              </div>

              <div className="form-group">
                <label>Correo</label>
                <input
                  type="email"
                  placeholder="correo@email.com"
                />
              </div>

              <div className="form-group">
                <label>Asunto</label>
                <input
                  type="text"
                  placeholder="Asunto del mensaje"
                />
              </div>

              <div className="form-group">
                <label>Mensaje</label>
                <textarea
                  rows="6"
                  placeholder="Escribe tu mensaje..."
                ></textarea>
              </div>

              <button type="submit" className="contact-btn">
                Enviar mensaje
              </button>

            </form>

          </div>

        </div>
      </section>

    </div>
  )
}

export default Contacto