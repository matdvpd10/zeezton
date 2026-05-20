import { Link } from 'react-router-dom'
import { motion } from "framer-motion";
import '../styles/home.css'

import fondoBMW from "../assets/home/fondo.jpg";
import coilovers from "../assets/home/coilovers.png";
import interiorImg from "../assets/home/interior.jpg";
import discosimg from "../assets/home/discos2.jpg";
import enmblemas from "../assets/home/emblemas.jpeg";
import iluminacion from "../assets/home/iluminacion1.jpg";

function Home() {

  return (
    <>

<section
  className="hero-zeezton"
  style={{
    backgroundImage: `url(${fondoBMW})`
  }}
>

        <div className="container">

          <span className="hero-badge">
            Unete a nuestra comunidad
          </span>

          <motion.h1
  className="hero-title"
  initial={{ opacity: 0, y: 50, scale: 0.95 }}
  animate={{ opacity: 1, y: 0, scale: 1 }}
  transition={{ duration: 0.8, ease: "easeOut" }}
>
  Zeezton Store
</motion.h1>

          <p className="hero-text">
            Repuestos, accesorios y estilo exclusivo para tu BMW.
          </p>

          <div className="d-flex gap-3 mt-4">

            <Link to="/productos" className="btn-shop">
  Ver Catalogo
  <span>→</span>
</Link>

            <Link
              to="/contacto"
              className="btn btn-outline-light"
            >
              Contactar
            </Link>

          </div>

        </div>

      </section>


<section className="home-info-section">

  <div className="container">

    <motion.div
      className="home-section-title"
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.25 }}
      transition={{
        duration: 0.7,
        ease: [0.22, 1, 0.36, 1]
      }}
    >

      <h2>Categorías destacadas</h2>

      <p>
        Explora nuestros accesorios BMW por categoría.
      </p>

    </motion.div>


    <div className="home-categories-grid">


      <motion.div
        className="home-category-card d-flex flex-column"
        initial={{ opacity: 0, y: 35 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.25 }}
        transition={{
          duration: 0.65,
          delay: 0.10,
          ease: [0.22, 1, 0.36, 1]
        }}
      >

        <img
          src={discosimg}
          alt="Performance BMW"
          className="img-fluid rounded-4 w-100 category-img mb-3"
        />

        <h3 className="mb-2">
          Performance
        </h3>

        <p className="mb-0">
          Mejoras para potencia, respuesta y conducción.
        </p>

      </motion.div>


      <motion.div
        className="home-category-card d-flex flex-column"
        initial={{ opacity: 0, y: 35 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.25 }}
        transition={{
          duration: 0.65,
          delay: 0.18,
          ease: [0.22, 1, 0.36, 1]
        }}
      >

        <img
          src={enmblemas}
          alt="Exterior BMW"
          className="img-fluid rounded-4 w-100 category-img mb-3"
        />

        <h3 className="mb-2">
          Exterior
        </h3>

        <p className="mb-0">
          Detalles deportivos, emblemas y estilo M.
        </p>

      </motion.div>


      <motion.div
        className="home-category-card d-flex flex-column"
        initial={{ opacity: 0, y: 35 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.25 }}
        transition={{
          duration: 0.65,
          delay: 0.26,
          ease: [0.22, 1, 0.36, 1]
        }}
      >

        <img
          src={iluminacion}
          alt="Iluminación BMW"
          className="img-fluid rounded-4 w-100 category-img mb-3"
        />

        <h3 className="mb-2">
          Iluminación
        </h3>

        <p className="mb-0">
          Accesorios modernos para destacar tu BMW.
        </p>

      </motion.div>


      <motion.div
        className="home-category-card d-flex flex-column"
        initial={{ opacity: 0, y: 35 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.25 }}
        transition={{
          duration: 0.65,
          delay: 0.34,
          ease: [0.22, 1, 0.36, 1]
        }}
      >

        <img
          src={interiorImg}
          alt="Interior BMW"
          className="img-fluid rounded-4 w-100 category-img mb-3"
        />

        <h3 className="mb-2">
          Interior
        </h3>

        <p className="mb-0">
          Comodidad, terminaciones y estética premium.
        </p>

      </motion.div>

    </div>

  </div>

</section>


<section className="home-quality-section">

  <div className="container home-quality-grid">

    <motion.div
      initial={{ opacity: 0, x: -60 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: false, amount: 0.3 }}
      transition={{ duration: 1.1, ease: "easeOut" }}
    >

      <h2>
        Calidad y estilo para tu BMW
      </h2>

      <p>
        Dale un estilo unico  a tu bmw con los nuevos coilovers maxpeedingrods, diseñados para ofrecer un rendimiento excepcional y una apariencia agresiva.
      </p>

      <ul>
        <li>Ajuste de dureza en 24 niveles</li>
        <li>Mejor estabilidad y control</li>
        <li>Mayor respuesta en curvas</li>
        <li>Construcción reforzada y durable</li>
      </ul>

    </motion.div>


    <motion.div
      className="home-quality-card"
      initial={{ opacity: 0, x: 60 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: false, amount: 0.3 }}
      transition={{ duration: 1.1, ease: "easeOut" }}
    >

      <img
        src={coilovers}
        alt="BMW Zeezton Store"
      />

    </motion.div>

  </div>

</section>

    </>
  )
}

export default Home