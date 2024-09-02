from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
contacts = []

@app.route('/')
def home():
    return render_template('contact.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if "@" not in email or not email.islower():
            return "Invalid email. Please enter a valid email address in lowercase."

        if password != confirm_password:
            return "Password do not match"

        users[username] = {'email': email, 'password': password}
        return redirect(url_for('login'))
    return render_template('sign_up.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            return redirect(url_for('landing_page'))
        else:
            return "Invalid username or password"
    return render_template('login.html')


@app.route('/add_contact', methods=['GET'])
def add_contact_form():
    return render_template('contact.html')


@app.route('/add_contact', methods=['POST'])
def new_contact():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']

        for contact in contacts:
            if contact['phone'] == phone:
                return "Contact already exists!"

        if "@" not in email or not email.islower():
            return "Invalid email. Please enter a valid email address in lowercase."

        if len(phone) != 11 or phone[0:3] not in ["080", "081", "070", "090", "091"]:
            return "Invalid phone number. Please enter a valid 11-digit phone number"

        contacts.append({'id': len(contacts) + 1, 'first_name': first_name, 'last_name': last_name, 'email': email, 'phone': phone})
        return "Contact saved successfully"
    return render_template('contact.html')

@app.route('/view_contacts', methods=['GET'])
def view_contacts():
    return render_template('view_contact.html', contacts=contacts)


@app.route('/edit_contact/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    for contact in contacts:
        if contact['id'] == contact_id:
            break
    else:
        contact = None

    if contact:
        if request.method == 'POST':
            contact['first_name'] = request.form['first_name']
            contact['last_name'] = request.form['last_name']
            contact['email'] = request.form['email']
            contact['phone'] = request.form['phone']
            return redirect(url_for('view_contacts'))
        return render_template('edit_contact.html', contact=contact)
    return "Contact not found!"


@app.route('/delete_contact/<int:contact_id>', methods=['GET', 'POST'])
def delete_contact(contact_id):
    for contact in contacts:
        if contact['id'] == contact_id:
            break
    else:
        contact = None

    if contact:
        contacts.remove(contact)
        return redirect(url_for('view_contacts'))
    return "Contact not found!"

@app.route('/search_contacts', methods=['GET'])
def search_contacts():
    query = request.args.get('query')
    if query:
        search_results = []
        for contact in contacts:
            if (query.lower() in contact['first_name'].lower() or
                    query.lower() in contact['last_name'].lower() or
                    query.lower() in contact['email'].lower()):
                search_results.append(contact)
        if search_results:
            return render_template('search_contact.html', search_results=search_results)
        else:
            return "No contacts found"
    return render_template('search_contact.html')

@app.route('/')
def landing_page():
    return render_template('landing.html')

if __name__ == '__main__':
    app.run(debug=True)