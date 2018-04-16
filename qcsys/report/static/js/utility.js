$('#c_status').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var qc_id = button.data('qcid') // Extract info from data-* attributes
  var modal = $(this)
  modal.find('.modal-title').text('案例 ' +qc_id + ' 状态修改')
  modal.find('#qcid-value').val(qc_id)
});

$('#c_processing').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var qc_id = button.data('qcid') // Extract info from data-* attributes
  var modal = $(this)
  modal.find('.modal-title').text('案例 ' +qc_id + ' 处理进度')
  modal.find('#qcid-value-p').val(qc_id)
});

$('#label_delete').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  console.log(button)
  var qc_id = button.data('qcid') // Extract info from data-* attributes
  console.log(qc_id)
  var modal = $(this)
  urlStr = modal.find('#del_c_label').attr('href')
  modal.find('#del_c_label').attr('href', urlStr + qc_id)
});

$('#attachment_delete').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  console.log(button)
  var qc_id = button.data('qcid') // Extract info from data-* attributes
  console.log(qc_id)
  var modal = $(this)
  urlStr = modal.find('#del_c_attach').attr('href')
  modal.find('#del_c_attach').attr('href', urlStr + qc_id)
});

$('[name="search_case"]').submit(function(){
    var input = $.trim($('#casesearch').val());
    if(input == ''){
        $('#casesearch').val('');
         return false;
    }
});


var btn = document.getElementById('submitbt');
var itemlist = document.getElementById('items');

if (btn != null){
    btn.addEventListener('click', addItem);
}
if (itemlist != null){
    itemlist.addEventListener('click', removeItem);
}


function addItem(e){
  e.preventDefault();
  // Get input value
  var newItem = document.getElementById('item-username').value;
  // Create new li element
  var span = document.createElement('span');
  span.className = 'badge badge-info label_sizing m-1';
  // Add text node with input value
  span.appendChild(document.createTextNode(newItem));
  // Append button to li
  var input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'handles[]';
  input.value = newItem + ';';
  span.appendChild(input);
  // Append li to list
  itemlist.appendChild(span);

//  document.getElementById('item').value = '';
}

function removeItem(e){
    if(e.target.classList.contains('label_sizing')){
        if(confirm('Are You Sure?')){
          var li = e.target;
          itemlist.removeChild(li);
        }
    }
}

var l_btn = document.getElementById('submitbt-labels');
var l_itemlist = document.getElementById('labelitems');

if (l_btn != null){
    l_btn.addEventListener('click', addLabelItem);
}
if (l_itemlist != null){
    l_itemlist.addEventListener('click', removeLabelItem);
}

function addLabelItem(e){
  e.preventDefault();
  // Get input value
  var newItem = document.getElementById('item-labels').value;
  // Create new li element
  var span = document.createElement('span');
  span.className = 'badge badge-info label_sizing m-1';
  // Add text node with input value
  span.appendChild(document.createTextNode(newItem));
  // Append button to li
  var input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'labels[]';
  input.value = newItem;
  span.appendChild(input);
  // Append li to list
  l_itemlist.appendChild(span);

//  document.getElementById('item').value = '';
}

function removeLabelItem(e){
    if(e.target.classList.contains('label_sizing')){
        if(confirm('Are You Sure?')){
          var li = e.target;
          l_itemlist.removeChild(li);
        }
    }
}

