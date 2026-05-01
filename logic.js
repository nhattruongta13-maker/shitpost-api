const API = 'https://shitpost-api-production.up.railway.app';
showBeardFact();
document.getElementById('post-btn').onclick = addPost;
document.getElementById('get-posts-btn').onclick = getPosts;
async function addPost(){
  let text = document.getElementById('post-text').value;
  if (text === '') return;
  
  const res = await fetch(`${API}/api/post`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({content: text})
  });
  const result = await res.json();
  console.log(result);
  
  // Just refresh from server instead of manual DOM
  document.getElementById('post-text').value = '';
  getPosts(); // <-- simpler + always in sync
}
async function showBeardFact(){
  try {
    const res = await fetch(`${API}/api/beard`);
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
  const res = await fetch(`${API}/api/post`);
  const data = await res.json();
  const container = document.getElementById('posts-list'); // needs new div in HTML
  container.innerHTML = '';
  data.forEach((post, index) => {
    container.innerHTML += `
      <div class="post">
        <span>${post}</span>
        <button onclick="deletePost(${index})">X</button>
      </div>`;
  });
}
async function deletePost(index){
  await fetch(`${API}/api/post/${index}`, { // <-- FIXED SLASH HERE
    method: 'DELETE' 
  });
  getPosts();
}