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
    let mv = id('mediaVideo'),
        mediaOptions = {
            video: {
            tag: 'video',
            type: 'video/webm',
            ext: '.mp4',
            gUM: {video: true, audio: true}
            },
            audio: {
            tag: 'audio',
            type: 'audio/wav',
            ext: '.wav',
            gUM: {audio: true}
            }
        };
    media = mv.checked ? mediaOptions.video : mediaOptions.audio;
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
        , hf = document.createElement('a')
    ;
    log(blob)
    
    mt.controls = true;
    mt.src = url;
    hf.href = url;
    hf.download = `${counter++}${media.ext}`;
    hf.innerHTML = `donwload ${hf.download}`;

    li.appendChild(mt);
    li.appendChild(hf);
    ul.appendChild(li);

    // $.ajax({
    //     type: "POST",
    //     url: "http://127.0.0.1:5000/api",
    //     data: `{
    //       "Id": 78912,
    //       "Customer": "Jason Sweet",
    //     }`,
    //     success: function (result) {
    //        console.log(result);
    //     },
    //     dataType: "json"
    // });
    
    // $.ajax({
    //     type: 'POST',
    //     dataType: 'json',
    //     url: "http://127.0.0.1:5000/api",
    //     // username: 'user',
    //     // password: 'pass',
    //     crossDomain: true,
    //     xhrFields: {
    //       withCredentials: true,
    //     },
    //     data: {
    //         "Id": 78912,
    //         "Customer": "Jason Sweet",
    //     },
    //   })
    //     .done(function (data) {
    //       console.log('done');
    //     })
    //     .fail(function (xhr, textStatus, errorThrown) {
    //       alert(xhr.responseText);
    //       alert(textStatus);
    // });
    // var data = new FormData()
    // data.append('file', blob , 'file')

    // fetch('http://127.0.0.1:8000/audioblob/', {
    //     method: 'POST',
    //     body: data

    // }).then(response => response.json()
    // ).then(json => {
    //     console.log(json)
    // });
    // var blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });

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
            console.log('response' + JSON.stringify(data));
        },
        error: function () {
        // handle error case here
        }
    })
}
