
document.getElementById('storyForm').addEventListener('submit', function(event) {
    event.preventDefault(); // 阻止表单的默认提交行为

    // 获取表单数据
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;

    // 创建故事元素
    const storyDiv = document.createElement('div');
    storyDiv.className = 'story';
    storyDiv.innerHTML = `<h4>${title}</h4><p>${content}</p>`;

    // 将故事元素添加到页面上
    document.getElementById('storiesContainer').appendChild(storyDiv);

    // 清空表单
    document.getElementById('storyForm').reset();
});