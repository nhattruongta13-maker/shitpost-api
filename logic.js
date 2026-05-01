showBeardFact();
document.getElementById('post-btn').onclick = addPost;
document.getElementById('get-posts-btn').onclick = getPosts;
async function addPost(){
    let text = document.getElementById('post-text').value; // Check this ID matches your HTML
    if (text === '') return;
    
    // This sends to Flask POST
    const res = await fetch('http://localhost:5000/api/post', {
        method: 'POST',
        headers: {'Content-Type' : 'application/json'},
        body: JSON.stringify({content: text})
    });
    
    const result = await res.json(); // Add this to see Flask response
    console.log(result); // Check browser console
    
    let newDiv = document.createElement('div');
    newDiv.className = 'post';
    newDiv.innerHTML = '<p>' + text + '</p>';
    let container = document.querySelector('.container');
    let form = document.getElementById('post2');
    container.insertBefore(newDiv, form);
    document.getElementById('post-text').value = '';
    saveAllPosts();
}

function saveAllPosts(){
    let containerHTML = document.querySelector('.container').innerHTML;
    localStorage.setItem('shitPosts', containerHTML);
}

async function showBeardFact(){
    try {
        const res = await fetch('http://localhost:5000/api/beard'); // GET
        const data = await res.json();
        
        let factDiv = document.createElement('h2');
        factDiv.innerText = data.text;
        factDiv.style.color = '#ff3b2f';
        document.querySelector('.fact').prepend(factDiv);
    } catch (err) {
        console.log("Beard fact failed:", err);
    }
}

async function getPosts(){
    const res = await fetch('http://localhost:5000/api/post');
    const data = await res.json();
    const container = document.querySelector('.container');

    container.innerHTML = '';
    data.forEach((post, index) => {
        container.innerHTML += `
        <div class="post">
            <span>${post}</span>
            <button onclick="deletePost(${index})">X</button>
        </div>`
    });
}

async function deletePost(index){
    await fetch(`http://localhost:5000/api/post/${index}`, {
        method: 'DELETE'
    });
    getPosts();
}

