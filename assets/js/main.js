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
  const codeBlocks = document.querySelectorAll('code');
  codeBlocks.forEach(block => {
    const container = document.createElement('div');
    container.className = 'code-container';
    
    const codeText = document.createElement('span');
    codeText.className = 'code-text';
    codeText.textContent = block.textContent;
    
    const copyIcon = document.createElement('span');
    copyIcon.className = 'copy-icon';
    copyIcon.title = '复制';
    copyIcon.onclick = () => copyToClipboard(block.textContent);
    
    container.appendChild(codeText);
    container.appendChild(copyIcon);
    
    block.parentNode.replaceChild(container, block);
  });
}); 