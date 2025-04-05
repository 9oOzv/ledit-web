
async function update_data(type, kvs) {
    console.debug('Updating', { type, kvs });
    const url = '/update'
    const data = {
        type: type,
        id: kvs['id'],
        fields: kvs,
    }
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (response.ok) {
            location.reload();
        } else {
            alert(await response.text());
        }
    } catch (error) {
        alert(error);
    }
}


function read_input(form_id, keys) {
    console.debug('Reading inputs', { form_id, keys });
    const kvs = {};
    for(const key of keys) {
        console.debug('Reading input', { form_id, key });
        const inputId = form_id + '-' + key;
        const v = document.getElementById(inputId).value;
        kvs[key] = v;
        console.debug('Found value', { key, v });
    }
    return kvs;
}


function get_keys(form_id) {
    console.debug('Getting keys', { form_id });
    return (
        document
        .getElementById(`${form_id}-keys`)
        .value
        .split(',')
    );
}

function get_type(form_id) {
    console.debug('Getting type', { form_id });
    return (
        document
        .getElementById(`${form_id}-type`)
        .value
    );
}


async function update(form_id) {
    console.info('Updating', { form_id });
    const keys = get_keys(form_id);
    const type = get_type(form_id);
    const kvs = read_input(form_id, keys);
    await update_data(type, kvs);
}
