# Testing Guide for WhatsApp Financial Planner Bot

This document provides instructions for testing the WhatsApp financial planner bot and its related components.

---

## Automated Testing

### Prerequisites

- Ensure all dependencies are installed (`npm install`).
- MongoDB server is running.
- Local AI inference server is running (`python3 local_ai_server.py`).
- Web application server is running (`node web_app_socket.js`).

### Running Tests

Run the automated test suite using Jest:

```bash
npm test
```

This will execute tests located in the `tests` directory, including:

- AI model integration tests
- Web API endpoint tests
- Bot message processing tests

---

## Manual Testing

### Setup

Ensure all services are running:

- MongoDB
- Local AI inference server
- Web application server
- WhatsApp bot

### Test Scenarios

1. **Record Income**

   Send a WhatsApp message to the bot:

   ```
   pemasukan 10000
   ```

   Expected response:

   ```
   Pemasukan sebesar Rp 10000 telah dicatat. Saldo Anda saat ini sebesar Rp <current_balance>.
   ```

   Verify the dashboard updates with the new balance.

2. **Record Outcome**

   Send a WhatsApp message:

   ```
   pengeluaran 5000
   ```

   Expected response:

   ```
   Pengeluaran sebesar Rp 5000 telah dicatat. Saldo Anda saat ini sebesar Rp <current_balance>.
   ```

3. **Request Report**

   Send a WhatsApp message:

   ```
   laporan
   ```

   Expected response:

   ```
   Laporan Keuangan:
   Pemasukan: Rp <total_income>
   Pengeluaran: Rp <total_outcome>
   Saldo: Rp <balance>

   Untuk laporan lengkap, kunjungi: http://localhost:5000
   ```

4. **Add Budget**

   Send a WhatsApp message:

   ```
   add budget groceries 200000 monthly
   ```

   Expected response:

   ```
   Budget untuk kategori 'groceries' sebesar Rp 200000 per monthly telah ditambahkan.
   ```

5. **Show Budgets**

   Send a WhatsApp message:

   ```
   show budgets
   ```

   Expected response:

   ```
   Daftar Budget:
   - groceries: Rp 200000 per monthly
   ```

6. **Add Goal**

   Send a WhatsApp message:

   ```
   add goal vacation 5000000
   ```

   Expected response:

   ```
   Goal 'vacation' dengan target Rp 5000000 telah ditambahkan.
   ```

7. **Show Goals**

   Send a WhatsApp message:

   ```
   show goals
   ```

   Expected response:

   ```
   Daftar Goals:
   - vacation: Target Rp 5000000, Saat ini Rp <current_amount>
   ```

---

## Troubleshooting

- Check logs in `financial_planner.log` for errors.
- Verify all services are running and accessible.
- Ensure network connectivity between components.

---

For further assistance, please contact the maintainer.
