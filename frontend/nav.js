// nav.js — toggling nav and auth-aware links
document.addEventListener('DOMContentLoaded', ()=>{
  const navToggle = document.getElementById('nav-toggle');
  const navLinks = document.getElementById('nav-links');
  const navLogin = document.getElementById('nav-login');
  const navRegister = document.getElementById('nav-register');
  const navLogout = document.getElementById('nav-logout');
  const logoutBtnTop = document.getElementById('logout-btn-top');

  if(navToggle) navToggle.addEventListener('click', ()=> navLinks.classList.toggle('open'));

  function updateAuthLinks(){
    const user = localStorage.getItem('wheatshield_user');
    if(!navLogin || !navRegister || !navLogout) return;
    if(user){
      navLogin.style.display='none';
      navRegister.style.display='none';
      navLogout.style.display='block';
    } else {
      navLogin.style.display='block';
      navRegister.style.display='block';
      navLogout.style.display='none';
    }
  }
  updateAuthLinks();

  if(logoutBtnTop){
    logoutBtnTop.addEventListener('click', ()=>{
      if(typeof logout === 'function'){ logout(); }
      else { localStorage.removeItem('wheatshield_user'); window.location.href='login.html'; }
      updateAuthLinks();
    });
  }

  // Highlight current nav link
  const current = window.location.pathname.split('/').pop();
  document.querySelectorAll('.nav-links a').forEach(a=>{
    const href = a.getAttribute('href');
    if(href === current || (current === '' && href === 'dashboard.html')) a.classList.add('active');
  });

});