import "./index.css";
import React, { useState } from "react";

function App() {
  return (
    <>
      <div className="video-container">
        <video
          src={process.env.PUBLIC_URL + "/video.mp4"}
          loop
          autoPlay
          muted
          playsInline
          poster="/fallback.jpg"
        />
        <div className="content-overlay">
          <NavBar />
          <div className="home-title">
            DNA<br />
            ENCRYPTION
          </div>
          <button
            className="scroll-btn"
            onClick={() =>
              document
                .getElementById("about-us")
                .scrollIntoView({ behavior: "smooth" })
            }
          >
            Learn More ↓
          </button>
        </div>
      </div>

      <AboutUs />
      <Objectives />
      <HowWeDidIt />
    </>
  );
}

function NavBar() {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <div className="menu-container">
          <img
            src={process.env.PUBLIC_URL + "/menu.png"}
            alt="Menu"
            className="menu-icon-img"
          />
          <div className="dropdown-menu">
            <a href="#home">Home</a>
            <a href="#about-us">About Us</a>
            <a href="#objectives">Objectives</a>
            <a href="#how-we-did-it">How We Did It</a>
            <a
              href="https://github.com/Sankalp-dasari/DNAVault"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub Repo
            </a>
          </div>
        </div>
      </div>
    </nav>
  );
}


function AboutUs() {
  return (
    <section className="about-us" id="about-us">
      <h2>About Us</h2>
      <div className="team-cards">
        <a
          href="https://www.linkedin.com/in/ishaan-jain-07a782299/"
          target="_blank"
          rel="noopener noreferrer"
          className="card block"
        >
          <img src="/ishaan.jpg" alt="Ishaan" />
          <h3>Ishaan Jain</h3>
          <p>
            I'm Ishaan Jain, a computer science student passionate about AI, cybersecurity, and full-stack development. I enjoy building innovative solutions that blend intelligent systems with practical design, and I'm always exploring new ways to solve real-world problems through tech.
          </p>
        </a>
        <a
          href="https://www.linkedin.com/in/aditya-sunke/"
          target="_blank"
          rel="noopener noreferrer"
          className="card block"
        >
          <img src="/aditya.jpeg" alt="Aditya" />
          <h3>Aditya Sunke</h3>
          <p>
            Hi I'm Aditya! I'm a Computer Science Major with a minor in Quantum Information Science and Engineering. I have experience in Java, Python and C. I also have experience with post-quantum cryptographic protocols, quantum algorithms and quantum frameworks. I am passionate about quantum technologies and their potential the solve complex world-problems.
          </p>
        </a>
        <a
          href="https://www.linkedin.com/in/lehar-sai-sankalp-dasari-188517288/"
          target="_blank"
          rel="noopener noreferrer"
          className="card block"
        >
          <img src="/sankalp.jpeg" alt="Sankalp" />
          <h3>Sankalp Dasari</h3>
          <p>
            Hi, I’m Sankalp Dasari, a Computer Science major with a minor in Cybersecurity. I have experience working with Java, Python, and C, and I’ve developed projects in AI/ML, Full Stack Development, Cryptography, Computer Vision, and Real-Time Image Tracking.
I’m passionate about building intelligent systems and applying AI to solve real-world problems that make a meaningful impact.
          </p>
        </a>
      </div>
    </section>
  );
}

function Objectives() {
  return (
    <section className="objectives" id="objectives">
      <h2 className="reveal"> Objective</h2>
      <div className="objective-content">
        <p className="reveal">
          In October 2023, over <strong>7 million</strong> user profiles from{" "}
          <strong>23andMe</strong> were exposed in a massive data breach (The
          Guardian). Less than two years later, the company filed for{" "}
          <strong>bankruptcy in March 2025</strong> (Reuters).
        </p>
        <p className="reveal">
          As cyberattacks grow more advanced and{" "}
          <strong>quantum computing</strong> threatens traditional encryption
          methods, our project responds with a future-ready solution: a hybrid
          cryptographic system that merges the speed of{" "}
          <strong>AES (Advanced Encryption Standard)</strong> with the
          resilience of <strong>Kyber</strong>, a post-quantum encryption
          scheme.
        </p>
        <p className="reveal">
          This platform demonstrates secure, end-to-end DNA sequence encryption
          using quantum-resistant cryptography. Specifically:
        </p>
        <ul className="reveal">
          <li>
            <strong>AES-128</strong> for fast, symmetric encryption of DNA
            data blocks.
          </li>
          <li>
            <strong>Kyber</strong> for secure post-quantum key exchange.
          </li>
        </ul>
        <p className="reveal">
          Designed for use in <strong>bioinformatics</strong>,{" "}
          <strong>healthcare</strong>, and <strong>genetic research</strong>,
          where data confidentiality is absolutely critical.
        </p>
      </div>
    </section>
  );
}

function HowWeDidIt() {
  const [currentStep, setCurrentStep] = useState(1);

  const steps = [
    {
      id: 1,
      title: "DNA Encoding",
      content: [
        "DNA sequences are mapped to binary using 2-bit representations (A → 00, G → 01, C → 10, T → 11).",
        "These are then grouped into 4x4 matrices, creating blocks ready for AES encryption."
      ],
    },
    {
      id: 2,
      title: "AES + Kyber Encryption",
      content: [
        "AES-128 encrypts the binary matrix using a symmetric key.",
        "Kyber, a post-quantum algorithm, is used to securely transmit the symmetric key."
      ],
    },
    {
      id: 3,
      title: "Decryption & Verification",
      content: [
        "Kyber is used to recover the AES key. The encrypted blocks are decrypted.",
        "The original DNA sequence is reconstructed, ensuring data integrity and privacy."
      ],
    },
    {
      id: 4,
      content: [
        <a
          key="github-button"
          href="https://github.com/Sankalp-dasari/DNAVault"
          target="_blank"
          rel="noopener noreferrer"
          className="github-button"
        >
          🚀 Check out the code!
        </a>,
      ],
    },
  ];

  return (
    <section className="how-we-did-it" id="how-we-did-it">
      <h2 className="reveal">How We Did It</h2>
      <div className="stepper-bar">
        {steps.map((step, index) => (
          <div key={step.id} className="step-wrapper">
            <div
              className={`step-icon ${
                currentStep >= step.id ? "active" : ""
              }`}
              onClick={() => setCurrentStep(step.id)}
            >
              {step.id}
            </div>
            {index < steps.length - 1 && (
              <div
                className={`step-line ${
                  currentStep > step.id ? "active" : ""
                }`}
              />
            )}
          </div>
        ))}
      </div>

      <div className="step-content">
        <h3>{steps[currentStep - 1].title}</h3>
        {steps[currentStep - 1].content.map((el, idx) => (
          <div key={idx}>{el}</div>
        ))}
      </div>
    </section>
  );
}

export default App;
