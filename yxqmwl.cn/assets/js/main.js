(function(){
  const btn=document.querySelector('.menu-toggle');
  const nav=document.querySelector('.site-nav');
  if(btn&&nav){
    btn.addEventListener('click',function(){
      const open=nav.classList.toggle('open');
      btn.setAttribute('aria-expanded',String(open));
    });
  }
  const path=location.pathname.endsWith('/')?'/':location.pathname;
  document.querySelectorAll('.site-nav a').forEach(a=>{
    const href=a.getAttribute('href');
    if(href===path || (path==='/'&&href==='/')) a.classList.add('active');
  });
})();
