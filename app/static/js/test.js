document.getElementById('togglePanelBtn').addEventListener('click', function() {
  var panel = document.getElementById('panel');
  var isOpen = panel.style.left === '0px'; // Проверяем, открыта ли панель
  panel.style.left = isOpen ? '-300px' : '0px'; // Если панель открыта, закрываем ее, иначе открываем
});

document.getElementById('closePanelBtn').addEventListener('click', function() {
  document.getElementById('panel').style.left = '-300px'; // Закрываем панель при клике на кнопку "Закрыть панель"
});
