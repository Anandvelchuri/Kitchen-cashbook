// Initialize entries from localStorage or empty array if none exists
let entries = JSON.parse(localStorage.getItem('entries')) || [];

// DOM elements
const form = document.getElementById('entry-form');
const entriesDiv = document.getElementById('entries');
const totalIncomeDiv = document.getElementById('total-income');
const totalExpenseDiv = document.getElementById('total-expense');
const totalBalanceDiv = document.getElementById('total-balance');

// Format currency
function formatCurrency(amount) {
    return '$' + parseFloat(amount).toLocaleString('en-AU', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

// Calculate and update totals
function updateTotals() {
    const totals = entries.reduce((acc, entry) => {
        if (entry.type === 'income') {
            acc.income += entry.amount;
        } else {
            acc.expense += entry.amount;
        }
        return acc;
    }, { income: 0, expense: 0 });

    const balance = totals.income - totals.expense;

    totalIncomeDiv.textContent = formatCurrency(totals.income);
    totalExpenseDiv.textContent = formatCurrency(totals.expense);
    totalBalanceDiv.textContent = formatCurrency(balance);

    // Save to localStorage
    localStorage.setItem('entries', JSON.stringify(entries));
}

// Create entry HTML
function createEntryElement(entry) {
    const div = document.createElement('div');
    div.className = 'entry';
    div.innerHTML = `
        <div class="entry-header">
            <div class="entry-amount ${entry.type}">${formatCurrency(entry.amount)}</div>
            <div class="entry-delete" data-id="${entry.id}">×</div>
        </div>
        <div class="entry-details">
            <strong>${entry.category}</strong>
            ${entry.note ? `<span> - ${entry.note}</span>` : ''}
            <div class="entry-date">${new Date(entry.timestamp).toLocaleString()}</div>
        </div>
    `;

    // Add delete functionality
    div.querySelector('.entry-delete').addEventListener('click', function() {
        if (confirm('Delete this entry?')) {
            const id = this.getAttribute('data-id');
            entries = entries.filter(e => e.id !== id);
            updateEntries();
        }
    });

    // Add swipe to delete for mobile
    let touchStartX = 0;
    let touchEndX = 0;

    div.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    div.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].screenX;
        const swipeDistance = touchEndX - touchStartX;

        if (swipeDistance < -100) { // Swipe left to delete
            if (confirm('Delete this entry?')) {
                const id = div.querySelector('.entry-delete').getAttribute('data-id');
                entries = entries.filter(e => e.id !== id);
                updateEntries();
            }
        }
    }, { passive: true });

    return div;
}

// Update entries display
function updateEntries() {
    // Sort entries by timestamp, most recent first
    entries.sort((a, b) => b.timestamp - a.timestamp);
    
    // Clear current entries
    entriesDiv.innerHTML = '';
    
    if (entries.length === 0) {
        entriesDiv.innerHTML = '<div class="no-entries">No entries yet</div>';
    } else {
        // Add entries to DOM
        entries.forEach(entry => {
            entriesDiv.appendChild(createEntryElement(entry));
        });
    }
    
    // Update totals
    updateTotals();
}

// Form submission handler
form.addEventListener('submit', function(e) {
    e.preventDefault();
    const submitBtn = e.target.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Adding...';

    try {
        // Get form values
        const type = document.getElementById('type').value;
        const amount = parseFloat(document.getElementById('amount').value);
        const category = document.getElementById('category').value;
        const note = document.getElementById('note').value.trim();

        // Create new entry
        const entry = {
            id: Date.now().toString(), // Use timestamp as unique ID
            type,
            amount,
            category,
            note,
            timestamp: Date.now()
        };

        // Add to entries array
        entries.unshift(entry);

        // Update display
        updateEntries();

        // Reset form
        form.reset();
    } catch (err) {
        console.error('Form submission error:', err);
        alert('Failed to add entry. Please try again.');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Add Entry';
    }
});

// Initial render
updateEntries();
