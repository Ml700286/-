// 获取所有可拖动元素和垃圾桶
const draggables = document.querySelectorAll('.draggable');
const trashBins = document.querySelectorAll('.trash-bin');

// 物品名称和垃圾桶类型）
const correctCategories = {
    'plastic-bottle': 'kehuishou',
    'food-waste': 'chuyu',
    'battery': 'youhai',
    'suliaobox': 'bukehuishou'
};

// 中文提示
const categoryChinese = {
    'kehuishou': '可回收物',
    'chuyu': '厨余垃圾',
    'youhai': '有害垃圾',
    'bukehuishou': '不可回收垃圾'
};

//初始状态
const itemStatus = {
    'plastic-bottle': false,
    'food-waste': false,
    'battery': false,
    'suliaobox': false
};

// 初始位置
const originalPositions = {};

// 保存每个物品的初始位置
draggables.forEach(item => {
    const src = item.src.split('/').pop().split('.')[0]; // 提取名称
    originalPositions[src] = {
        left: item.style.left,
        bottom: item.style.bottom
    };
});

// 拖动样式
draggables.forEach(item => {
    item.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', e.target.src); // 传输图片地址
        e.target.classList.add('dragging'); // 添加拖拽样式
    });

    // 拖动结束：移除样式
    item.addEventListener('dragend', (e) => {
        e.target.classList.remove('dragging');
    });
});


trashBins.forEach(bin => {

    bin.addEventListener('dragover', (e) => {
        e.preventDefault();
        bin.style.transform = 'scale(1.2)';
    });

    // 拖拽离开时恢复
    bin.addEventListener('dragleave', () => {
        bin.style.transform = 'scale(1)';
    });

    bin.addEventListener('drop', (e) => {
        e.preventDefault();
        bin.style.transform = 'scale(1)';

        const itemSrc = e.dataTransfer.getData('text/plain');// 获取拖拽物品信息
        const itemName = itemSrc.split('/').pop().split('.')[0]; // 提取名称
        const draggedItem = document.querySelector(`.draggable[src*="${itemName}"]`); // 获取被拖动的元素

        // 获取垃圾桶类型和正确类型
        const binType = bin.dataset.type;
        const correctType = correctCategories[itemName];

        // 判断是否投放正确
        if (binType === correctType) {
            // 正确：隐藏物品并更新状态
            draggedItem.style.opacity = '0';
            itemStatus[itemName] = true;

            // 检查是否全部正确
            const allCorrect = Object.values(itemStatus).every(status => status);
            if (allCorrect) {
                alert('投放成功，感谢您的环保行为！');
                location.reload();
            }
        } else {
            alert(`投放错误！正确分类应为：${categoryChinese[correctType]}`);
            draggedItem.style.left = originalPositions[itemName].left;
            draggedItem.style.bottom = originalPositions[itemName].bottom;
            draggedItem.style.opacity = '1';
        }
    });
});

const images = document.querySelectorAll('.item img');

// 判断图片是否进入可视区域
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// 滚动事件监听
window.addEventListener('scroll', () => {
    images.forEach((img) => {
        if (isInViewport(img)) {
            img.classList.add('animate'); // 如果图片进入可视区域，添加动画类
        } else {
            img.classList.remove('animate'); // 如果图片离开可视区域，移除动画类
        }
    });
});

// 页面加载时触发一次
window.addEventListener('DOMContentLoaded', () => {
    window.dispatchEvent(new Event('scroll'));
});