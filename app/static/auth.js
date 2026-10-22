function createParticles(){

    const bg =
    document.querySelector(".bg-animation");

    if(!bg) return;

    for(let i=0;i<60;i++){

        const s =
        document.createElement("span");

        s.style.left =
        Math.random()*100 + "%";

        s.style.animationDuration =
        (10 + Math.random()*12)+"s";

        s.style.animationDelay =
        Math.random()*10+"s";

        bg.appendChild(s);

    }
}

document.addEventListener(
"DOMContentLoaded",
createParticles
);