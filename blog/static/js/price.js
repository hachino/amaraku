'use strict';

{
    function pointkangen(){
        // alert(Cookies.get('marathon'));
        const mcpoint = Cookies.get('marathon');
        if (mcpoint){
            // alert(mcpoint);
            document.querySelector('#marathon').options[mcpoint].selected = true;
        }

        const scpoint = Cookies.get('spu');
        if (scpoint){
            // alert(mcpoint);
            document.querySelector('#spu').options[scpoint].selected = true;
        }

        const marathon = Number(document.querySelector('#marathon').value);
        const spu = Number(document.querySelector('#spu').value);
        const goto = document.querySelector('#goto').textContent;
        
        const pointrate = 1-(marathon + spu + Number(goto))/100;
        
        document.querySelectorAll('#rakp').forEach((p,index) => {
            p.nextElementSibling.textContent = Math.floor(p.firstChild.textContent * pointrate);
        });
    }

    function cookiepoint(){
        const element = document.querySelector('#marathon');
        const elements = element.options;
        elements[5].selected = true;
    }

    // window.onload = cookiepoint;
    window.onload = pointkangen;
}

{
    document.querySelector('#price').addEventListener('click', () => {       
        
        const marathon = Number(document.querySelector('#marathon').value);
        Cookies.set('marathon', marathon);

        const spu = Number(document.querySelector('#spu').value);
        Cookies.set('spu', spu);
        
        const goto = document.querySelector('#goto').textContent;

        const pointrate = 1-(marathon + spu + Number(goto))/100;

        document.querySelectorAll('#rakp').forEach((p,index) => {
            p.nextElementSibling.textContent = Math.floor(p.firstChild.textContent * pointrate);
        });
    });
}

