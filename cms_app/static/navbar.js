// Navbar smooth scrolling
window.addEventListener("scroll", function () {
    const navbars = document.querySelectorAll(".navbar");
    navbars.forEach((navbar) => {
      if (window.scrollY > 100) {
        navbar.classList.add("opaque");
        navbar.classList.add("small-logo");
      } else {
        navbar.classList.remove("opaque");
        navbar.classList.remove("small-logo");
      }
    });
  });
  
  // Sidebar toggle functions
  function openSidebar() {
    document.getElementById("sidebar").style.right = "0";
  }
  
  function closeSidebar() {
    document.getElementById("sidebar").style.right = "-250px";
  }
  
  // Handle dropdown functionality
  document.addEventListener("DOMContentLoaded", function () {
    console.log("Navbar script loaded"); // Debugging log
  
    function attachDropdownListeners() {
      console.log("Attaching dropdown event listeners..."); // Debugging log
  
      const dropdownBtns = document.querySelectorAll(".dropdown-btn");
      dropdownBtns.forEach((btn) => {
        btn.addEventListener("click", function () {
          console.log("Dropdown clicked!"); // Debugging log
          this.classList.toggle("active");
          const submenu = this.nextElementSibling;
          submenu.style.display = submenu.style.display === "block" ? "none" : "block";
        });
      });
    }
  
    // Run when navbar is fully injected
    if (document.getElementById("navbar")) {
      setTimeout(attachDropdownListeners, 200); // Small delay to ensure elements exist
    }
  });
  
  