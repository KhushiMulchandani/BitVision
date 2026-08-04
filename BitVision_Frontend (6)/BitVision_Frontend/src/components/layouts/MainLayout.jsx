import Navbar from "../layout/Navbar";
import Sidebar from "../layout/Sidebar";
import Footer from "../layout/Footer";

function MainLayout() {
  return (
    <>
      <Navbar />

      <div className="main-wrapper">
        <Sidebar />

        <main className="content">
          Dashboard
        </main>
      </div>

      <Footer />
    </>
  );
}

export default MainLayout;