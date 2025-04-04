
async function update_data(type, id, kvs) {
    console.debug('Updating', { type, id, kvs });
    const url = '/update'
    const data = {
        type: type,
        id: id,
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


function read_input(type, id, keys) {
    console.debug('Reading inputs', { type, id, keys });
    const kvs = {};
    for(const key of keys) {
        console.debug('Reading input', { type, id, key });
        const inputId = type + '-' + id + '-' + key;
        const v = document.getElementById(inputId).value;
        kvs[key] = v;
        console.debug('Found value', { key, v });
    }
    return kvs;
}


function get_keys(type, id) {
    console.debug('Getting keys', { type, id });
    return (
        document
        .getElementById(`${type}-${id}-keys`)
        .value
        .split(',')
    );
}


async function update(type, id) {
    console.info('Updating', type, id);
    const keys = get_keys(type, id);
    const kvs = read_input(type, id, keys);
    await update_data(type, id, kvs);
}
