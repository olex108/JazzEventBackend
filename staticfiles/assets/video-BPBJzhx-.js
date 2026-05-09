const p=()=>{const i=document.querySelectorAll(".video-container"),n=e=>{const s=e.querySelector(".playBtn"),l=e.querySelector(".videoOverlay"),r=e.querySelector(".iframe-target");r&&(r.innerHTML="",r.classList.add("hidden")),s?.classList.remove("opacity-0","pointer-events-none"),l?.classList.remove("opacity-0")};i.forEach(e=>{const s=e.querySelector(".playBtn"),l=e.querySelector(".heroVideo"),r=e.querySelector(".iframe-target"),a=e.dataset.vkUrl;if(!r||!s)return;const d=t=>{i.forEach(o=>{o!==t&&n(o)})},c=()=>{if(d(e),!a)return;const t=a.includes("?"),o=a.includes("autoplay")?a:`${a}${t?"&":"?"}autoplay=1`;r.innerHTML=`
                <iframe src="${o}"
                        class="absolute inset-0 w-full h-full z-20"
                        allow="autoplay; encrypted-media; fullscreen; picture-in-picture;"
                        frameborder="0"
                        allowfullscreen>
                </iframe>`,r.classList.remove("hidden"),s.classList.add("opacity-0","pointer-events-none"),e.querySelector(".videoOverlay")?.classList.add("opacity-0")};s.addEventListener("click",t=>{t.preventDefault(),t.stopPropagation(),c()}),l?.addEventListener("click",t=>{t.preventDefault(),t.stopPropagation(),c()})})};export{p as i};
