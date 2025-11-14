<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>P&L Analyzer for Home Delivery — Web App</title>

  <!-- Bootstrap 5 for layout -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

  <!-- Chart.js for charts -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>

  <style>
    body { background:#f7f9fc; }
    .container-main { max-width:1100px; margin:30px auto; }
    pre.report { background:#0f172a; color:#e6eef8; padding:20px; border-radius:6px; font-family:Courier, monospace; font-size:13px; white-space:pre-wrap; }
    .card { box-shadow: 0 6px 18px rgba(16,24,40,0.06); }
    footer small { color: #6b7280; }
    .btn-export { white-space:nowrap; }
  </style>
</head>
<body>
  <div class="container-main">
    <h2 class="mb-3">P&L Analyzer for Home Delivery — Web App</h2>

    <div class="row g-3">
      <!-- Left column: Forms -->
      <div class="col-lg-5">
        <div class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">1. Enter Order Data</h5>
            <form id="orderForm" onsubmit="return false;">
              <div class="mb-2"><small class="text-muted">Revenue</small></div>
              <div class="mb-2 input-group">
                <span class="input-group-text">Product Sales ($)</span>
                <input type="number" step="0.01" class="form-control" id="product_sales" value="0.00" required>
              </div>
              <div class="mb-2 input-group">
                <span class="input-group-text">Delivery Fee ($)</span>
                <input type="number" step="0.01" class="form-control" id="delivery_fee" value="0.00" required>
              </div>
              <div class="mb-2 input-group">
                <span class="input-group-text">Other Fees ($)</span>
                <input type="number" step="0.01" class="form-control" id="other_fees" value="0.00" required>
              </div>
              <div class="mb-2 input-group">
                <span class="input-group-text">Discounts ($)</span>
                <input type="number" step="0.01" class="form-control" id="discounts" value="0.00" required>
              </div>

              <hr />
              <div class="mb-2"><small class="text-muted">COGS</small></div>
              <div class="mb-2 input-group">
                <span class="input-group-text">Product Cost ($)</span>
                <input type="number" step="0.01" class="form-control" id="cogs" value="0.00" required>
              </div>
              <div class="mb-2 input-group">
                <span class="input-group-text">Packaging Cost ($)</span>
                <input type="number" step="0.01" class="form-control" id="packaging_cost" value="0.00" required>
              </div>

              <div class="d-flex gap-2 mt-3">
                <button class="btn btn-primary" id="addOrderBtn">Add Order</button>
                <button class="btn btn-secondary" id="clearOrderBtn" type="button">Clear</button>
                <div class="ms-auto">
                  <button class="btn btn-outline-success btn-export" id="exportOrdersBtn" type="button">Export Orders CSV</button>
                  <label class="btn btn-outline-secondary btn-export mb-0">
                    Import Orders CSV <input type="file" id="importOrdersFile" accept=".csv" hidden>
                  </label>
                </div>
              </div>

              <div class="mt-3">
                <small class="text-muted">Orders stored locally in your browser (localStorage). Use export/import to move data between devices.</small>
              </div>
            </form>
          </div>
        </div>

        <div class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">2. Enter Monthly Expenses</h5>
            <form id="expensesForm" onsubmit="return false;">
              <div class="mb-2 input-group">
                <span class="input-group-text">People Costs ($)</span>
                <input type="number" step="0.01" class="form-control" id="people_costs" value="0.00" required>
              </div>
              <div class="mb-2 input-group">
                <span class="input-group-text">Delivery & Vehicle ($)</span>
                <input type="number" step="0.01" class="form-control" id="delivery_vehicle_costs" value="0.00" required>
              </div>
              <div class="mb-2 input-group">
                <span class="input-group-text">Technology ($)</span>
                <input type="number" step="0.01" class="form-control" id="technology_costs" value="0.00" required>
              </div>
              <div class="mb-2 input-group">
                <span class="input-group-text">Marketing ($)</span>
                <input type="number" step="0.01" class="form-control" id="marketing_costs" value="0.00" required>
              </div>
              <div class="mb-2 input-group">
                <span class="input-group-text">Rent & Utilities ($)</span>
                <input type="number" step="0.01" class="form-control" id="rent_utilities" value="0.00" required>
              </div>
              <div class="mb-2 input-group">
                <span class="input-group-text">Other Overhead ($)</span>
                <input type="number" step="0.01" class="form-control" id="other_overhead" value="0.00" required>
              </div>

              <div class="d-flex gap-2 mt-3">
                <button class="btn btn-success" id="saveExpensesBtn">Save Monthly Expenses</button>
                <button class="btn btn-secondary" id="clearExpensesBtn" type="button">Clear</button>
                <div class="ms-auto">
                  <button class="btn btn-outline-success btn-export" id="exportExpensesBtn" type="button">Export Expenses CSV</button>
                  <label class="btn btn-outline-secondary btn-export mb-0">
                    Import Expenses CSV <input type="file" id="importExpensesFile" accept=".csv" hidden>
                  </label>
                </div>
              </div>
              <div class="mt-2">
                <small id="expensesSavedLabel" class="text-muted">No expenses saved yet.</small>
              </div>
            </form>
          </div>
        </div>

        <div class="card">
          <div class="card-body">
            <h6>Orders Preview</h6>
            <div class="table-responsive" style="max-height:200px; overflow:auto;">
              <table class="table table-sm" id="ordersTable">
                <thead class="table-light">
                  <tr>
                    <th>#</th><th>Date</th><th>Product</th><th>Delivery</th><th>Other</th><th>Discount</th><th>COGS</th><th>Pack</th><th>Actions</th>
                  </tr>
                </thead>
                <tbody id="ordersTbody"></tbody>
              </table>
            </div>
            <div class="d-flex justify-content-between mt-2">
              <div><small id="ordersCountLabel" class="text-muted">0 orders</small></div>
              <div><button class="btn btn-danger btn-sm" id="clearAllOrdersBtn">Clear All Orders</button></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right column: Report + Charts -->
      <div class="col-lg-7">
        <div class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">3. Analysis & Report</h5>
            <div class="d-flex gap-2 mb-3">
              <button class="btn btn-primary" id="generateReportBtn">Generate P&L Report</button>
              <button class="btn btn-outline-primary" id="printReportBtn">Print Report</button>
              <button class="btn btn-outline-secondary" id="clearReportBtn">Clear Report</button>
            </div>

            <div class="mb-3">
              <canvas id="plChart" height="140"></canvas>
            </div>

            <div>
              <pre id="reportOutput" class="report">Click "Generate P&L Report" to begin.</pre>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-body">
            <h6>Quick Helpers</h6>
            <div class="d-flex flex-wrap gap-2">
              <button class="btn btn-outline-info btn-sm" id="downloadSummaryCSV">Download Summary CSV</button>
              <button class="btn btn-outline-warning btn-sm" id="resetAllBtn">Reset All (clear localStorage)</button>
            </div>
            <div class="mt-2">
              <small class="text-muted">Data is stored locally (browser). Export to CSV if you want a physical backup.</small>
            </div>
          </div>
        </div>

        <footer class="mt-3">
          <small>Built from your Tkinter script — converted to a single-file HTML/JS app. No back-end required.</small>
        </footer>
      </div>
    </div>
  </div>

<script>
/*
  P&L Analyzer — browser version
  - Stores data in localStorage (orders and the most recent expenses row)
  - CSV export/import supported
  - Chart shows total revenue and total COGS
  - Report text mirrors the structure from your Python app
*/

const ORDERS_KEY = 'pl_analyzer_orders_v1';
const EXPENSES_KEY = 'pl_analyzer_expenses_v1';

// Utilities
function safeFloat(v){ const f = parseFloat(v); return Number.isFinite(f) ? f : 0; }
function nowISO(){ return new Date().toISOString().slice(0,19).replace('T',' '); }
function loadOrders(){ try { return JSON.parse(localStorage.getItem(ORDERS_KEY) || '[]'); } catch(e){ return []; } }
function saveOrders(arr){ localStorage.setItem(ORDERS_KEY, JSON.stringify(arr)); }
function loadExpenses(){ try { return JSON.parse(localStorage.getItem(EXPENSES_KEY) || 'null'); } catch(e){ return null; } }
function saveExpenses(obj){ localStorage.setItem(EXPENSES_KEY, JSON.stringify(obj)); }
function formatMoney(v){ return Number(v).toLocaleString(undefined,{minimumFractionDigits:2, maximumFractionDigits:2}); }

// Initial rendering
document.addEventListener('DOMContentLoaded', () => {
  renderOrdersTable();
  loadExpensesToForm();
  initEventHandlers();
  drawEmptyChart();
});

// Event handlers
function initEventHandlers(){
  document.getElementById('addOrderBtn').addEventListener('click', addOrder);
  document.getElementById('clearOrderBtn').addEventListener('click', clearOrderForm);
  document.getElementById('saveExpensesBtn').addEventListener('click', saveExpenses);
  document.getElementById('clearExpensesBtn').addEventListener('click', clearExpensesForm);
  document.getElementById('generateReportBtn').addEventListener('click', generateReport);
  document.getElementById('printReportBtn').addEventListener('click', () => { window.print(); });
  document.getElementById('clearReportBtn').addEventListener('click', () => { document.getElementById('reportOutput').textContent = ''; });
  document.getElementById('clearAllOrdersBtn').addEventListener('click', clearAllOrders);
  document.getElementById('resetAllBtn').addEventListener('click', resetAllData);
  document.getElementById('exportOrdersBtn').addEventListener('click', exportOrdersCSV);
  document.getElementById('exportExpensesBtn').addEventListener('click', exportExpensesCSV);
  document.getElementById('importOrdersFile').addEventListener('change', importOrdersCSV);
  document.getElementById('importExpensesFile').addEventListener('change', importExpensesCSV);
  document.getElementById('downloadSummaryCSV').addEventListener('click', downloadSummaryCSV);
}

// Form helpers
function clearOrderForm(){
  ['product_sales','delivery_fee','other_fees','discounts','cogs','packaging_cost'].forEach(id => {
    document.getElementById(id).value = '0.00';
  });
}
function clearExpensesForm(){
  ['people_costs','delivery_vehicle_costs','technology_costs','marketing_costs','rent_utilities','other_overhead'].forEach(id => {
    document.getElementById(id).value = '0.00';
  });
}

// Add an order
function addOrder(){
  try {
    const order = {
      date: nowISO(),
      product_sales: safeFloat(document.getElementById('product_sales').value),
      delivery_fee: safeFloat(document.getElementById('delivery_fee').value),
      other_fees: safeFloat(document.getElementById('other_fees').value),
      discounts: safeFloat(document.getElementById('discounts').value),
      cogs: safeFloat(document.getElementById('cogs').value),
      packaging_cost: safeFloat(document.getElementById('packaging_cost').value)
    };
    const orders = loadOrders();
    orders.push(order);
    saveOrders(orders);
    renderOrdersTable();
    clearOrderForm();
    showTempMessage(`Order added — total orders: ${orders.length}`);
  } catch(e){
    alert('Error adding order. Check inputs.');
  }
}

// Render orders preview
function renderOrdersTable(){
  const tbody = document.getElementById('ordersTbody');
  tbody.innerHTML = '';
  const orders = loadOrders();
  orders.forEach((o, idx) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${idx+1}</td>
      <td style="min-width:120px">${o.date}</td>
      <td>${formatMoney(o.product_sales)}</td>
      <td>${formatMoney(o.delivery_fee)}</td>
      <td>${formatMoney(o.other_fees)}</td>
      <td>${formatMoney(o.discounts)}</td>
      <td>${formatMoney(o.cogs)}</td>
      <td>${formatMoney(o.packaging_cost)}</td>
      <td>
        <button class="btn btn-sm btn-outline-danger" onclick="deleteOrder(${idx})">Delete</button>
      </td>`;
    tbody.appendChild(tr);
  });
  document.getElementById('ordersCountLabel').textContent = `${orders.length} order(s)`;
}

// Delete single order
function deleteOrder(idx){
  if(!confirm('Delete this order?')) return;
  const orders = loadOrders();
  orders.splice(idx,1);
  saveOrders(orders);
  renderOrdersTable();
}

// Clear all orders
function clearAllOrders(){
  if(!confirm('Clear ALL orders permanently?')) return;
  localStorage.removeItem(ORDERS_KEY);
  renderOrdersTable();
  showTempMessage('All orders cleared.');
}

// Save expenses
function saveExpenses(){
  try {
    const obj = {
      date_saved: nowISO(),
      people_costs: safeFloat(document.getElementById('people_costs').value),
      delivery_vehicle_costs: safeFloat(document.getElementById('delivery_vehicle_costs').value),
      technology_costs: safeFloat(document.getElementById('technology_costs').value),
      marketing_costs: safeFloat(document.getElementById('marketing_costs').value),
      rent_utilities: safeFloat(document.getElementById('rent_utilities').value),
      other_overhead: safeFloat(document.getElementById('other_overhead').value)
    };
    saveExpenses(obj);
    document.getElementById('expensesSavedLabel').textContent = 'Last saved on: ' + obj.date_saved;
    showTempMessage('Monthly expenses saved.');
  } catch(e){
    alert('Error saving expenses.');
  }
}

function loadExpensesToForm(){
  const e = loadExpenses();
  if(!e) return;
  document.getElementById('people_costs').value = formatMoney(e.people_costs);
  document.getElementById('delivery_vehicle_costs').value = formatMoney(e.delivery_vehicle_costs);
  document.getElementById('technology_costs').value = formatMoney(e.technology_costs);
  document.getElementById('marketing_costs').value = formatMoney(e.marketing_costs);
  document.getElementById('rent_utilities').value = formatMoney(e.rent_utilities);
  document.getElementById('other_overhead').value = formatMoney(e.other_overhead);
  document.getElementById('expensesSavedLabel').textContent = 'Last saved on: ' + e.date_saved;
}

// Generate the P&L report
function generateReport(){
  const orders = loadOrders();
  const expenses = loadExpenses();

  if(!orders || orders.length === 0){
    alert('No order data available. Please add orders first.');
    return;
  }
  if(!expenses){
    alert('No expense data available. Please save monthly expenses first.');
    return;
  }

  // Revenue
  const total_product_sales = orders.reduce((s,o) => s + safeFloat(o.product_sales), 0);
  const total_delivery_fees = orders.reduce((s,o) => s + safeFloat(o.delivery_fee), 0);
  const total_other_fees = orders.reduce((s,o) => s + safeFloat(o.other_fees), 0);
  const total_discounts = orders.reduce((s,o) => s + safeFloat(o.discounts), 0);
  const total_revenue = total_product_sales + total_delivery_fees + total_other_fees - total_discounts;

  // COGS
  const total_cogs = orders.reduce((s,o) => s + safeFloat(o.cogs) + safeFloat(o.packaging_cost), 0);

  // Gross Profit
  const gross_profit = total_revenue - total_cogs;
  const gross_profit_margin = total_revenue > 0 ? (gross_profit / total_revenue * 100) : 0;

  // Operating Expenses (sum of all expense fields)
  const total_expenses = safeFloat(expenses.people_costs) + safeFloat(expenses.delivery_vehicle_costs) +
    safeFloat(expenses.technology_costs) + safeFloat(expenses.marketing_costs) +
    safeFloat(expenses.rent_utilities) + safeFloat(expenses.other_overhead);

  // Net Profit
  const net_profit = gross_profit - total_expenses;

  // KPIs
  const num_orders = orders.length;
  const avg_order_value = num_orders > 0 ? (total_revenue / num_orders) : 0;
  const total_delivery_costs = safeFloat(expenses.delivery_vehicle_costs);
  const cost_per_delivery = num_orders > 0 ? (total_delivery_costs / num_orders) : 0;
  const avg_delivery_fee_collected = num_orders > 0 ? (total_delivery_fees / num_orders) : 0;
  const people_costs = safeFloat(expenses.people_costs);
  const labor_cost_percent = total_revenue > 0 ? (people_costs / total_revenue * 100) : 0;

  // Compose report text (monospaced)
  const line = '='.repeat(90);
  let report = `${line}\n${'PROFIT & LOSS (P&L) REPORT'.padStart(47)}\n${line}\n\n`;
  report += `--- FINANCIAL SUMMARY ---\n`;
  report += `Total Revenue:                      $${formatMoney(total_revenue)}\n`;
  report += `  - Product Sales:                  $${formatMoney(total_product_sales)}\n`;
  report += `  - Delivery Fees:                  $${formatMoney(total_delivery_fees)}\n`;
  report += `  - Other Fees:                     $${formatMoney(total_other_fees)}\n`;
  report += `  - Discounts:                      ($${formatMoney(total_discounts)})\n`;
  report += `${'-'.repeat(50)}\n`;
  report += `Cost of Goods Sold (COGS):          ($${formatMoney(total_cogs)})\n`;
  report += `${'='.repeat(50)}\n`;
  report += `Gross Profit:                       $${formatMoney(gross_profit)}\n`;
  report += `Gross Profit Margin:                ${gross_profit_margin.toFixed(2)}%\n\n`;
  report += `Operating Expenses:                 ($${formatMoney(total_expenses)})\n`;
  report += `  - People Costs:                   ($${formatMoney(people_costs)})\n`;
  report += `  - Delivery & Vehicle Costs:       ($${formatMoney(total_delivery_costs)})\n`;
  report += `  - Technology Costs:               ($${formatMoney(expenses.technology_costs)})\n`;
  report += `  - Marketing Costs:                ($${formatMoney(expenses.marketing_costs)})\n`;
  report += `  - Rent & Utilities:               ($${formatMoney(expenses.rent_utilities)})\n`;
  report += `  - Other Overhead:                 ($${formatMoney(expenses.other_overhead)})\n`;
  report += `${'-'.repeat(50)}\n`;
  report += `NET PROFIT / (LOSS):                $${formatMoney(net_profit)}\n\n`;
  report += `${line}\n${'KEY PERFORMANCE METRICS'.padStart(47)}\n${line}\n`;
  report += `Total Number of Orders:             ${num_orders}\n`;
  report += `Average Order Value (AOV):          $${formatMoney(avg_order_value)}\n`;
  report += `Average Delivery Fee Collected:     $${formatMoney(avg_delivery_fee_collected)}\n`;
  report += `Calculated Cost Per Delivery:       $${formatMoney(cost_per_delivery)}\n`;
  report += `Labor Cost as % of Revenue:         ${labor_cost_percent.toFixed(2)}%\n\n`;
  report += `${line}\n${'SYSTEM ANALYSIS & SUGGESTIONS'.padStart(47)}\n${line}\n`;

  // Suggestions logic (mirror your Python logic)
  let suggestions = '';
  if(net_profit >= 0){
    suggestions += '\n>>> CONGRATULATIONS! You are profitable. <<<\n\nTo improve further:\n';
    if(gross_profit_margin < 50) suggestions += '- Consider increasing prices or finding cheaper suppliers to boost your Gross Profit Margin.\n';
    if(labor_cost_percent > 30) suggestions += '- Your labor costs are a bit high. Look into optimizing staff schedules.\n';
  } else {
    suggestions += '\n>>> ACTION REQUIRED: You are currently operating at a loss. <<<\n\nHere are the most likely problem areas and what to change:\n\n';
    if(gross_profit_margin < 40){
      suggestions += `[PROBLEM] Low Gross Profit Margin (${gross_profit_margin.toFixed(2)}%). Your core service is not profitable.\n`;
      suggestions += '  [SUGGESTION] RAISE PRICES: Increase product prices or delivery fees.\n';
      suggestions += '  [SUGGESTION] CUT COGS: Negotiate with suppliers for better prices or reduce waste.\n\n';
    }
    if(cost_per_delivery > avg_delivery_fee_collected){
      suggestions += '[PROBLEM] Delivery costs are higher than the fees you collect.\n';
      suggestions += '  [SUGGESTION] INCREASE FEES: Raise your delivery fee or set a minimum order value for delivery.\n';
      suggestions += '  [SUGGESTION] OPTIMIZE ROUTES: Use routing software to save fuel and time.\n\n';
    }
    if(labor_cost_percent > 35){
      suggestions += `[PROBLEM] High labor costs (${labor_cost_percent.toFixed(2)}% of revenue).\n`;
      suggestions += '  [SUGGESTION] OPTIMIZE SCHEDULING: Schedule more staff during peak hours and fewer during slow times.\n';
      suggestions += '  [SUGGESTION] IMPROVE EFFICIENCY: Train staff to handle calls and deliveries faster.\n\n';
    }
    const marketing_cost = safeFloat(expenses.marketing_costs);
    if(marketing_cost > 0 && total_revenue > 0 && (marketing_cost / total_revenue) > 0.10){
      suggestions += '[PROBLEM] High marketing spend relative to revenue.\n';
      suggestions += '  [SUGGESTION] FOCUS ON ROI: Stop ads that are not bringing in customers. Track your marketing results.\n\n';
    }
  }
  if(!suggestions) suggestions = 'No specific suggestions at this time. Continue monitoring your metrics.\n';
  report += suggestions;

  document.getElementById('reportOutput').textContent = report;
  updateChart(total_revenue, total_cogs);
}

// Chart (Revenue vs COGS)
let plChart = null;
function drawEmptyChart(){
  const ctx = document.getElementById('plChart').getContext('2d');
  plChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Revenue','COGS'],
      datasets: [{ label: 'Amount ($)', data: [0,0], backgroundColor: ['rgba(0,123,255,0.6)','rgba(255,99,132,0.6)'], borderWidth:1 }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: { y: { beginAtZero:true } }
    }
  });
}

function updateChart(revenue, cogs){
  if(!plChart) return;
  plChart.data.datasets[0].data = [parseFloat(revenue.toFixed(2)), parseFloat(cogs.toFixed(2))];
  plChart.update();
}

// CSV export/import helpers
function arrayToCSV(rows){
  return rows.map(r => r.map(cell => {
    if (typeof cell === 'string' && (cell.includes(',') || cell.includes('"') || cell.includes('\n'))) {
      return `"${cell.replace(/"/g,'""')}"`;
    }
    return String(cell);
  }).join(',')).join('\n');
}

function exportOrdersCSV(){
  const orders = loadOrders();
  if(!orders || orders.length === 0){ alert('No orders to export.'); return; }
  const header = ['date','product_sales','delivery_fee','other_fees','discounts','cogs','packaging_cost'];
  const rows = [header].concat(orders.map(o => header.map(h => o[h])));
  const csv = arrayToCSV(rows);
  downloadTextFile(csv, `orders_${new Date().toISOString().slice(0,10)}.csv`);
}

function exportExpensesCSV(){
  const e = loadExpenses();
  if(!e){ alert('No expenses to export.'); return; }
  const header = ['date_saved','people_costs','delivery_vehicle_costs','technology_costs','marketing_costs','rent_utilities','other_overhead'];
  const rows = [header, header.map(h => e[h])];
  const csv = arrayToCSV(rows);
  downloadTextFile(csv, `expenses_${new Date().toISOString().slice(0,10)}.csv`);
}

function downloadTextFile(text, filename){
  const blob = new Blob([text], {type:'text/csv;charset=utf-8;'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

// Import orders CSV
function importOrdersCSV(e){
  const file = e.target.files[0];
  if(!file) return;
  const reader = new FileReader();
  reader.onload = evt => {
    const text = evt.target.result;
    const rows = parseCSV(text);
    if(rows.length < 2){ alert('CSV seems empty or only headers.'); return; }
    const header = rows[0].map(h => h.trim());
    const expected = ['date','product_sales','delivery_fee','other_fees','discounts','cogs','packaging_cost'];
    // Basic header check (not strict)
    const hasAll = expected.every(h => header.includes(h));
    if(!hasAll) {
      if(!confirm('CSV headers do not match expected order fields. Try to import anyway?')) return;
    }
    const data = rows.slice(1).map(r => {
      const obj = {};
      header.forEach((h,i) => obj[h] = r[i] ?? '');
      // ensure numeric fields
      expected.slice(1).forEach(k => obj[k] = safeFloat(obj[k]));
      return obj;
    });
    saveOrders(data);
    renderOrdersTable();
    showTempMessage('Orders imported.');
  };
  reader.readAsText(file);
  e.target.value = '';
}

// Import expenses CSV
function importExpensesCSV(e){
  const file = e.target.files[0];
  if(!file) return;
  const reader = new FileReader();
  reader.onload = evt => {
    const text = evt.target.result;
    const rows = parseCSV(text);
    if(rows.length < 2){ alert('CSV seems empty or only headers.'); return; }
    const header = rows[0].map(h => h.trim());
    const row = rows[1];
    const expenses = {};
    header.forEach((h,i) => {
      const val = row[i] ?? '';
      expenses[h] = (h === 'date_saved') ? val : safeFloat(val);
    });
    if(!expenses.date_saved) expenses.date_saved = nowISO();
    saveExpenses(expenses);
    loadExpensesToForm();
    showTempMessage('Expenses imported.');
  };
  reader.readAsText(file);
  e.target.value = '';
}

// Very simple CSV parser (handles quoted fields)
function parseCSV(text){
  const rows = [];
  let cur = '';
  let row = [];
  let inQuotes = false;
  for(let i=0;i<text.length;i++){
    const ch = text[i];
    if(inQuotes){
      if(ch === '"'){
        if(text[i+1] === '"'){ cur += '"'; i++; } else { inQuotes = false; }
      } else { cur += ch; }
    } else {
      if(ch === '"'){ inQuotes = true; }
      else if(ch === ','){ row.push(cur); cur = ''; }
      else if(ch === '\r'){ continue; }
      else if(ch === '\n'){ row.push(cur); rows.push(row); row = []; cur = ''; }
      else { cur += ch; }
    }
  }
  // final row
  if(cur !== '' || row.length > 0) { row.push(cur); rows.push(row); }
  return rows;
}

// Reset everything
function resetAllData(){
  if(!confirm('Reset all saved data? This will clear orders and expenses from localStorage.')) return;
  localStorage.removeItem(ORDERS_KEY);
  localStorage.removeItem(EXPENSES_KEY);
  renderOrdersTable();
  document.getElementById('reportOutput').textContent = '';
  loadExpensesToForm();
  showTempMessage('All app data cleared.');
}

// Summary CSV (simple export of aggregated metrics)
function downloadSummaryCSV(){
  const orders = loadOrders();
  const expenses = loadExpenses();
  if(!orders || orders.length === 0 || !expenses){ alert('Please ensure you have orders and saved expenses before exporting summary.'); return; }

  // compute metrics same as generateReport
  const total_product_sales = orders.reduce((s,o) => s + safeFloat(o.product_sales), 0);
  const total_delivery_fees = orders.reduce((s,o) => s + safeFloat(o.delivery_fee), 0);
  const total_other_fees = orders.reduce((s,o) => s + safeFloat(o.other_fees), 0);
  const total_discounts = orders.reduce((s,o) => s + safeFloat(o.discounts), 0);
  const total_revenue = total_product_sales + total_delivery_fees + total_other_fees - total_discounts;
  const total_cogs = orders.reduce((s,o) => s + safeFloat(o.cogs) + safeFloat(o.packaging_cost), 0);
  const gross_profit = total_revenue - total_cogs;
  const total_expenses = safeFloat(expenses.people_costs) + safeFloat(expenses.delivery_vehicle_costs) + safeFloat(expenses.technology_costs) + safeFloat(expenses.marketing_costs) + safeFloat(expenses.rent_utilities) + safeFloat(expenses.other_overhead);
  const net_profit = gross_profit - total_expenses;
  const header = ['metric','value'];
  const rows = [
    header,
    ['date', new Date().toISOString()],
    ['num_orders', orders.length],
    ['total_revenue', total_revenue],
    ['total_cogs', total_cogs],
    ['gross_profit', gross_profit],
    ['total_expenses', total_expenses],
    ['net_profit', net_profit]
  ];
  const csv = arrayToCSV(rows);
  downloadTextFile(csv, `pl_summary_${new Date().toISOString().slice(0,10)}.csv`);
}

// Small UI helper
function showTempMessage(msg){
  // simple temporary status via alert-like small top bar
  const prev = document.getElementById('tempMsg');
  if(prev) prev.remove();
  const div = document.createElement('div');
  div.id = 'tempMsg';
  div.style.position = 'fixed';
  div.style.right = '20px';
  div.style.bottom = '20px';
  div.style.zIndex = '9999';
  div.innerHTML = `<div class="toast show align-items-center text-bg-dark border-0"><div class="d-flex"><div class="toast-body">${msg}</div><button type="button" class="btn-close btn-close-white me-2 m-auto" onclick="this.parentElement.parentElement.remove()"></button></div></div>`;
  document.body.appendChild(div);
  setTimeout(()=>{ if(div) div.remove(); }, 4000);
}
</script>
</body>
</html>
