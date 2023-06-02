const OPENAI_API_KEY = 'PUT YOUR API KEY HERE'

async function translate(text) {
    const prompt = `Translate this into Simplified Chinese:\n\n${text}\n\n`
    const body = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 100,
        "temperature": 0
    }
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + OPENAI_API_KEY,
        },
        body: JSON.stringify(body),
    }
    const response = await fetch('https://api.openai.com/v1/completions', options)
    const json = await response.json()
    return json.choices[0].text
}

function show(x, y, text, translateText) {
    let container = document.createElement('div')
    container.innerHTML = `
    <header>翻译<span class="close">X</span></header>
    <main>
      <div class="source">
        <div class="title">原文</div>
        <div class="content">${text}</div>
      </div>
      <div class="dest">
        <div class="title">简体中文</div>
        <div class="content">${translateText}</div>
      </div>
    </main>
    `
    container.classList.add('translate-panel')
	container.classList.add('show')
    container.style.left = x + 'px'
    container.style.top = y + 'px'
    document.body.appendChild(container)

	let close = container.querySelector('.close')
	close.onclick = () => {
        container.classList.remove('show')
    }
}

window.onmouseup = async function (e) {

    // 非左键，不处理
    if (e.button != 0) {
        return;
    }
    
    // 未选中文本，不处理
    let text = window.getSelection().toString().trim()
    if (!text) {
        return;
    }

    // 翻译选中文本
    let translateText = await translate(text)

    // 在鼠标位置显示翻译结果
    show(e.pageX, e.pageY, text, translateText)
}
