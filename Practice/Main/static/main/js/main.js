var count = 1;

function plus(){
    let p = document.getElementById('target')
    let ul = document.createElement('ul')
    let li_one = document.createElement('li')

    let label_track = document.createElement('label')
    label_track.innerText = 'Название: '
    let input_track = document.createElement('input')
    input_track.name = 'name_track' + count
    input_track.type = 'text'

    let li_two = document.createElement('li')

    let label_file = document.createElement('label')
    label_file.innerText = 'Путь: '
    let input_file = document.createElement('input')
    input_file.name = 'url' + count
    count += 1
    input_file.type = 'file'

    li_one.appendChild(label_track)
    li_one.appendChild(input_track)
    li_two.appendChild(label_file)
    li_two.appendChild(input_file)

    ul.appendChild(li_one)
    ul.appendChild(li_two)

    p.before(ul)
};
