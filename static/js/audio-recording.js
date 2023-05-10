'use strict'

let log = console.log.bind(console),
id = val => document.getElementById(val),
ul = id('ul'),
gUMbtn = id('gUMbtn'),
start = id('start'),
stop = id('stop'),
stream,
recorder,
counter=1,
chunks,
media;


gUMbtn.onclick = e => {
    media = {
        tag: 'audio',
        type: 'audio/wav',
        ext: '.wav',
        gUM: {audio: true}
    };
    
    navigator.mediaDevices.getUserMedia(media.gUM).then(_stream => {
        stream = _stream;
        id('gUMArea').style.display = 'none';
        id('btns').style.display = 'inherit';
        start.removeAttribute('disabled');
        recorder = new MediaRecorder(stream);
        recorder.ondataavailable = e => {
            chunks.push(e.data);
            if(recorder.state == 'inactive')  makeLink();
        };
        log('got media successfully');
        }).catch(log);
}

start.onclick = e => {
    start.disabled = true;
    stop.removeAttribute('disabled');
    chunks=[];
    recorder.start();
}


stop.onclick = e => {
    stop.disabled = true;
    recorder.stop();
    start.removeAttribute('disabled');
    log("stopped")

}



function makeLink(){
    let blob = new Blob(chunks, {type: media.type })
        , url = URL.createObjectURL(blob)
        , li = document.createElement('li')
        , mt = document.createElement(media.tag)
        // , hf = document.createElement('a')
    ;
    log(blob)
    
    mt.controls = true;
    mt.src = url;
    // hf.href = url;
    // hf.download = `${counter++}${media.ext}`;
    // hf.innerHTML = `donwload ${hf.download}`;

    li.classList.add('bg-yellow', 'text-left');
    li.appendChild(mt);
    // li.appendChild(hf);
    ul.appendChild(li);

    console.log("start sending binary data...");
    var form = new FormData();
    form.append('audio', blob);

    $.ajax({
        url: 'http://localhost:8000/audioblob/',
        type: 'POST',
        data: form,
        processData: false,
        contentType: false,
        success: function (data) {
            console.log(JSON.stringify(data));
            let li = document.createElement('li')
            let p = document.createElement('p')
            p.innerHTML = data
            p.classList.add('text-right');
            li.appendChild(p)
            ul.appendChild(li)
        },
        error: function (e) {
            console.log('error' + e)
        }
    })
}