from uuid import uuid4
from flask import Flask, jsonify, request

from model.blockchain import BlockChain

app = Flask(__name__)

node_id = str(uuid4()).replace('-', '')  # このノードのグローバルにユニークなアドレスを作る
bc = BlockChain()  # ブロックチェーンクラスを初期化


@app.route('/transactions/new', methods=['POST'])
def post_new_transactions():
    values = request.get_json()

    # POSTされたデータに必要なデータがあるかを確認
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # 新しいトランザクションを作る
    index = bc.new_transaction(values['sender'], values['recipient'], values['amount'])

    res = {
        'message': f'トランザクションはブロック {index} に追加されました',
    }
    return jsonify(res), 201


@app.route('/mine')
def get_mine():
    # 次のプルーフを見つけるためプルーフ・オブ・ワークアルゴリズムを使用する
    last_proof = bc.last_block['proof']
    proof = bc.proof_of_work(last_proof)

    # プルーフを見つけたことに対する報酬を得る
    # 送信者は、採掘者が新しいコインを採掘したことを表すために"0"とする
    bc.new_transaction(
        sender="0",
        recipient=node_id,
        amount=1,
    )

    # チェーンに新しいブロックを加えることで、新しいブロックを採掘する
    block = bc.new_block(proof)

    res = {
        'message': '新しいブロックを採掘しました',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(res), 200


@app.route('/chain')
def get_full_chain():
    res = {
        'chain': bc.chain,
        'length': len(bc.chain),
    }
    return jsonify(res), 200


@app.route('/nodes/register', methods=['POST'])
def register_node():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: 有効ではないノードのリストです", 400

    for node in nodes:
        bc.register_node(node)

    res = {
        'message': '新しいノードが追加されました',
        'total_nodes': list(bc.nodes),
    }
    return jsonify(res), 201


@app.route('/nodes/resolve')
def consensus():
    replaced = bc.resolve_conflicts()
    if replaced:
        res = {
            'message': 'チェーンが置き換えられました',
            'new_chain': bc.chain
        }
    else:
        res = {
            'message': 'チェーンが確認されました',
            'chain': bc.chain
        }
    return jsonify(res), 200


if __name__ == '__main__':
    app.run()
