import "./ModelsHeader.css";

function ModelsHeader() {

  return (

    <section className="models-header">

      <div className="models-header-left">

        <span className="models-badge">

          AI Research Lab

        </span>

        <h1>

          AI Models

        </h1>

        <p>

          Compare the machine learning models powering
          BitVision's Bitcoin prediction engine.

        </p>

      </div>

      <div className="models-status">

        <span className="status-dot"></span>

        5 Models Active

      </div>

    </section>

  );

}

export default ModelsHeader;