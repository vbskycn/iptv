function copyToClipboard(text) {
  const input = document.createElement('textarea');
  input.value = text;
  document.body.appendChild(input);
  input.select();
  document.execCommand('copy');
  document.body.removeChild(input);
  alert('已复制到剪贴板');
}

// 为所有代码块添加复制图标
document.addEventListener('DOMContentLoaded', function() {
  // 选择所有代码块容器
  const codeBlocks = document.querySelectorAll('.language-plaintext.highlighter-rouge');
  
  codeBlocks.forEach(block => {
    // 获取代码内容
    const codeElement = block.querySelector('code');
    const codeText = codeElement.textContent.trim();
    
    // 创建复制图标容器
    const copyContainer = document.createElement('div');
    copyContainer.className = 'copy-container';
    copyContainer.style.position = 'relative';
    
    // 创建复制图标
    const copyIcon = document.createElement('span');
    copyIcon.className = 'copy-icon';
    copyIcon.title = '复制';
    copyIcon.style.position = 'absolute';
    copyIcon.style.right = '10px';
    copyIcon.style.top = '10px';
    copyIcon.onclick = () => copyToClipboard(codeText);
    
    // 调整代码块容器样式
    block.style.position = 'relative';
    
    // 将复制图标添加到代码块中
    copyContainer.appendChild(copyIcon);
    block.insertBefore(copyContainer, block.firstChild);
  });
}); 