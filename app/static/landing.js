document
.querySelectorAll('.agent-card')
.forEach(card=>{

card.addEventListener('mousemove',e=>{

const rect =
card.getBoundingClientRect();

const x =
e.clientX - rect.left;

const y =
e.clientY - rect.top;

card.style.transform =
`rotateX(${(y-100)/15}deg)
 rotateY(${(x-100)/15}deg)
 translateY(-10px)`;

});

card.addEventListener(
'mouseleave',
()=>{
card.style.transform='';
});
});