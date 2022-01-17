import * as schemawax from 'schemawax';

const sendRequest = <T>(request: RequestInfo, decoder: schemawax.Decoder<T>): Promise<T> =>
    new Promise((resolve, reject) => {
        fetch(request).then(response => {
            if (response.ok) {
                response.json()
                    .then(json => {
                        const result = decoder.decode(json);

                        if (result === null) {
                            reject(`Unable to deserialize response: ${JSON.stringify(json)}`);
                        } else {
                            resolve(result);
                        }
                    })
                    .catch(() => reject('Unable to deserialize response'));
            } else {
                response.text()
                    .then(message => reject(message))
                    .catch(error => reject(error));
            }
        });
    });

export const http = {
    sendRequest
};
