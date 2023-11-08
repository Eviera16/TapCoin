from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegistrationSerializer, GetUserSerializer, LoginSerializer
from ..models import *
from decouple import config
import binascii
import os
import bcrypt
import requests
from random import randrange
import datetime
import time
from datetime import timedelta
from django.utils.timezone import make_aware
from web3 import Web3

ganache_rpc_url = 'http://127.0.0.1:8545'
w3 = Web3(Web3.HTTPProvider(ganache_rpc_url))
queue_name = "A"
queue_A_count = 1
queue_B_count = 1
queue_C_count = 1
queue_D_count = 1

contract_abi_const = [{'inputs': [{'internalType': 'address', 'name': '_taptapCoinAddress', 'type': 'address'}, {'internalType': 'address', 'name': '_priceFeedAddress', 'type': 'address'}], 'stateMutability': 'nonpayable', 'type': 'constructor', 'name': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'string', 'name': '_message', 'type': 'string'}], 'name': 'CheckingEvent', 'type': 'event'}, {'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'previousOwner', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'newOwner', 'type': 'address'}], 'name': 'OwnershipTransferred', 'type': 'event'}, {'inputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'activePlayers', 'outputs': [{'internalType': 'address payable', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'addActivePlayer', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'newAccount', 'type': 'address'}, {'internalType': 'string', 'name': 'code', 'type': 'string'}], 'name': 'addWallet', 'outputs': [{'internalType': 'address payable[]', 'name': '', 'type': 'address[]'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'addresses', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'winner', 'type': 'address'}], 'name': 'awardTapTapCoin', 'outputs': [], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'winner', 'type': 'address'}, {'internalType': 'uint256', 'name': 'percentage', 'type': 'uint256'}], 'name': 'calculateWinnings', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'checkForUser', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'checkUserFaceIdChecked', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'checkUserIsActive', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'string', 'name': 'str1', 'type': 'string'}, {'internalType': 'string', 'name': 'str2', 'type': 'string'}], 'name': 'compare', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'pure', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}, {'internalType': 'string', 'name': 'code', 'type': 'string'}, {'internalType': 'uint256', 'name': 'transaction_price', 'type': 'uint256'}], 'name': 'faceIdCheck', 'outputs': [{'components': [{'internalType': 'uint256', 'name': 'wins', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'games', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'waitTimeStart', 'type': 'uint256'}, {'internalType': 'bool', 'name': 'faceIdCheck', 'type': 'bool'}, {'internalType': 'bool', 'name': 'isValidUser', 'type': 'bool'}, {'internalType': 'bool', 'name': 'isValidFaceId', 'type': 'bool'}, {'internalType': 'bool', 'name': 'isActive', 'type': 'bool'}, {'internalType': 'bool', 'name': 'isWinner', 'type': 'bool'}, {'internalType': 'bool', 'name': 'isAboveZero', 'type': 'bool'}, {'internalType': 'bool', 'name': 'has100Games', 'type': 'bool'}, {'internalType': 'bool', 'name': 'skipping', 'type': 'bool'}, {'components': [{'internalType': 'uint256', 'name': 'addWalletTransaction', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'faceIdCheckTransaction', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_1', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_2', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_3', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_4', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_5', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'totalTransactionAmount', 'type': 'uint256'}, {'internalType': 'bool', 'name': 'hasTotalTransactions', 'type': 'bool'}], 'internalType': 'struct TapCoinGame.TotalTransactions', 'name': 'totalTransactions', 'type': 'tuple'}], 'internalType': 'struct TapCoinGame.streakBoardValues', 'name': '', 'type': 'tuple'}], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'getCurrentActualUsdOneCentCost', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'getPrice', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'getTotalTapTapCoinSupply', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}, {'internalType': 'uint256', 'name': 'dataIndex', 'type': 'uint256'}], 'name': 'getTransactionData', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'getUsersGamesCount', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'getUsersStreakCount', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'owner', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'name': 'playerIndexes', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address[]', 'name': 'users', 'type': 'address[]'}], 'name': 'removeActivePlayer', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'renounceOwnership', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'user', 'type': 'address'}], 'name': 'setUsersGamesTo100', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'name': 'streakBoard', 'outputs': [{'internalType': 'uint256', 'name': 'wins', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'games', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'waitTimeStart', 'type': 'uint256'}, {'internalType': 'bool', 'name': 'faceIdCheck', 'type': 'bool'}, {'internalType': 'bool', 'name': 'isValidUser', 'type': 'bool'}, {'internalType': 'bool', 'name': 'isValidFaceId', 'type': 'bool'}, {'internalType': 'bool', 'name': 'isActive', 'type': 'bool'}, {'internalType': 'bool', 'name': 'isWinner', 'type': 'bool'}, {'internalType': 'bool', 'name': 'isAboveZero', 'type': 'bool'}, {'internalType': 'bool', 'name': 'has100Games', 'type': 'bool'}, {'internalType': 'bool', 'name': 'skipping', 'type': 'bool'}, {'components': [{'internalType': 'uint256', 'name': 'addWalletTransaction', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'faceIdCheckTransaction', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_1', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_2', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_3', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_4', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_5', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'totalTransactionAmount', 'type': 'uint256'}, {'internalType': 'bool', 'name': 'hasTotalTransactions', 'type': 'bool'}], 'internalType': 'struct TapCoinGame.TotalTransactions', 'name': 'totalTransactions', 'type': 'tuple'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'taptapCoin', 'outputs': [{'internalType': 'contract IERC20', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'testFunction', 'outputs': [{'internalType': 'address payable[]', 'name': '', 'type': 'address[]'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'newOwner', 'type': 'address'}], 'name': 'transferOwnership', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'winner', 'type': 'address'}, {'internalType': 'address', 'name': 'loser', 'type': 'address'}, {'internalType': 'uint256', 'name': 'transaction_price_winner', 'type': 'uint256'}, {'internalType': 'uint256', 'name': 'transaction_price_loser', 'type': 'uint256'}, {'internalType': 'bool', 'name': 'isDevEnv', 'type': 'bool'}, {'internalType': 'uint256', 'name': 'percentage', 'type': 'uint256'}], 'name': 'updatePlayersWins', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'nonpayable', 'type': 'function'}]
contract_byte_code = "6080604052600436106101815760003560e01c80638da5cb5b116100d1578063b24f768c1161008a578063dbe13d7511610064578063dbe13d75146104d7578063e16b4a9b146106a6578063f2fde38b146106c8578063f434e94f146106e857600080fd5b8063b24f768c14610477578063b55f108f14610497578063c28aafb1146104b757600080fd5b80638da5cb5b1461036f578063916287951461038d5780639895ece4146103ba57806398d5fdca146103cf5780639eee624a146103e4578063a8b34a391461043b57600080fd5b80633a96fdd71161013e578063715018a611610118578063715018a6146102c9578063745b4b3b146102de5780638236e6161461031657806382542aa91461033657600080fd5b80633a96fdd7146102695780634c10b79c1461028957806364a48696146102a957600080fd5b8063039e7a71146101865780630f966112146101ae5780631d3345f2146101ce57806324a30c25146101fe578063326418b7146102205780633a0ef37114610256575b600080fd5b34801561019257600080fd5b5061019b610708565b6040519081526020015b60405180910390f35b3480156101ba57600080fd5b5061019b6101c9366004611df1565b61077b565b3480156101da57600080fd5b506101ee6101e9366004611e1b565b610881565b60405190151581526020016101a5565b34801561020a57600080fd5b5061021e610219366004611e84565b6108a9565b005b34801561022c57600080fd5b5061019b61023b366004611e1b565b6001600160a01b031660009081526006602052604090205490565b61021e610264366004611e1b565b610abb565b34801561027557600080fd5b506101ee610284366004611fa1565b610b96565b34801561029557600080fd5b5061019b6102a4366004611e1b565b610c00565b3480156102b557600080fd5b506101ee6102c4366004611e1b565b610c5a565b3480156102d557600080fd5b5061021e610c80565b3480156102ea57600080fd5b506001546102fe906001600160a01b031681565b6040516001600160a01b0390911681526020016101a5565b34801561032257600080fd5b5061019b610331366004612005565b610ce6565b34801561034257600080fd5b5061019b610351366004611e1b565b6001600160a01b031660009081526006602052604090206001015490565b34801561037b57600080fd5b506000546001600160a01b03166102fe565b34801561039957600080fd5b5061019b6103a8366004611e1b565b60076020526000908152604090205481565b3480156103c657600080fd5b5061019b611211565b3480156103db57600080fd5b5061019b61124c565b3480156103f057600080fd5b5061021e6103ff366004611e1b565b6001600160a01b031660009081526006602052604090206064600182015560038101805460ff60301b1916600160301b17905542600290910155565b34801561044757600080fd5b506101ee610456366004611e1b565b6001600160a01b031660009081526006602052604090206003015460ff1690565b34801561048357600080fd5b5061019b610492366004611df1565b6112e3565b3480156104a357600080fd5b506102fe6104b236600461206d565b611436565b3480156104c357600080fd5b5061021e6104d2366004612086565b611460565b3480156104e357600080fd5b506105d66104f2366004611e1b565b60066020818152600092835260409283902080546001820154600283015460038401548751610120810189526004860154815260058601549681019690965295840154968501969096526007830154606085015260088301546080850152600983015460a0850152600a83015460c0850152600b83015460e0850152600c9092015460ff90811615156101008581019190915291959294929381841693928304821692620100008104831692630100000082048116926401000000008304821692650100000000008104831692600160301b8204811692600160381b90920416908c565b604080519c8d526020808e019c909c528c81019a909a529715156060808d01919091529615156080808d019190915295151560a0808d019190915294151560c0808d019190915293151560e0808d0191909152921515610100808d01919091529115156101208c015215156101408b015286516101608b0152978601516101808a0152958501516101a0890152928401516101c0880152908301516101e08701528201516102008601528101516102208501529081015161024084015201511515610260820152610280016101a5565b3480156106b257600080fd5b506106bb611601565b6040516101a591906120f6565b3480156106d457600080fd5b5061021e6106e3366004611e1b565b611621565b3480156106f457600080fd5b5061021e610703366004612129565b6116ec565b600154604080516318160ddd60e01b815290516000926001600160a01b0316916318160ddd9160048083019260209291908290030181865afa158015610752573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906107769190612180565b905090565b6001600160a01b0382166000908152600660205260408120600c015460ff1615156001146108245760405162461bcd60e51b815260206004820152604560248201527f596f7520646f206e6f74206861766520612076616c6964207472616e7361637460448201527f696f6e20616d6f756e7420746f2063616c63756c617465207468652077696e6e60648201526434b733b99760d91b608482015260a4015b60405180910390fd5b6001600160a01b0383166000908152600660205260408120600b8101546005820154600490920154909291610858916121af565b9050600061086682846121af565b905060006108748287611936565b9450505050505b92915050565b6001600160a01b03166000908152600660205260409020600301546301000000900460ff1690565b60005b8151811015610ab757600660008383815181106108cb576108cb6121c7565b60200260200101516001600160a01b03166001600160a01b0316815260200190815260200160002060030160019054906101000a900460ff1615610aa557600060076000848481518110610921576109216121c7565b60200260200101516001600160a01b03166001600160a01b031681526020019081526020016000205490506000600160088054905061096091906121dd565b9050600060088281548110610977576109776121c7565b6000918252602082200154600880546001600160a01b03909216935090859081106109a4576109a46121c7565b600091825260209091200154600880546001600160a01b0390921692508391869081106109d3576109d36121c7565b9060005260206000200160006101000a8154816001600160a01b0302191690836001600160a01b031602179055508360076000888881518110610a1857610a186121c7565b60200260200101516001600160a01b03166001600160a01b031681526020019081526020016000208190555060076000826001600160a01b03166001600160a01b03168152602001908152602001600020600090556008805480610a7e57610a7e6121f4565b600082815260209020810160001990810180546001600160a01b0319169055019055505050505b80610aaf8161220a565b9150506108ac565b5050565b6001600160a01b038116600090815260076020526040812054600880549091908110610ae957610ae96121c7565b60009182526020822001546040516001600160a01b0390911692508190839034908381818185875af1925050503d8060008114610b42576040519150601f19603f3d011682016040523d82523d6000602084013e610b47565b606091505b509150915081610b905760405162461bcd60e51b81526020600482015260146024820152732330b4b632b2103a379039b2b7321022ba3432b960611b604482015260640161081b565b50505050565b60008151835114610ba95750600061087b565b81604051602001610bba9190612223565b6040516020818303038152906040528051906020012083604051602001610be19190612223565b6040516020818303038152906040528051906020012014905092915050565b600880546001808201835560008381527ff3f7a9fe364faab93b216da50a3214154f22a0a2b415b23a84c8169e8b636ee390920180546001600160a01b0319166001600160a01b0386161790559154909161087b916121dd565b6001600160a01b0316600090815260066020526040902060030154610100900460ff1690565b6000546001600160a01b03163314610cda5760405162461bcd60e51b815260206004820181905260248201527f4f776e61626c653a2063616c6c6572206973206e6f7420746865206f776e6572604482015260640161081b565b610ce4600061195e565b565b6000610cf187610c5a565b1515600114610d515760405162461bcd60e51b815260206004820152602660248201527f5468652057696e6e696e67206163636f756e74206973206e6f742072656769736044820152653a32b932b21760d11b606482015260840161081b565b610d5a86610c5a565b1515600114610db95760405162461bcd60e51b815260206004820152602560248201527f546865204c6f73696e67206163636f756e74206973206e6f742072656769737460448201526432b932b21760d91b606482015260840161081b565b610dc287610881565b1515600114610e1e5760405162461bcd60e51b815260206004820152602260248201527f5468652057696e6e696e67206163636f756e74206973206e6f74206163746976604482015261329760f11b606482015260840161081b565b610e2786610881565b1515600114610e825760405162461bcd60e51b815260206004820152602160248201527f546865204c6f73696e67206163636f756e74206973206e6f74206163746976656044820152601760f91b606482015260840161081b565b6001600160a01b03871660009081526006602052604090206003015460ff161515600114610f0f5760405162461bcd60e51b815260206004820152603460248201527f5468652057696e6e696e67206163636f756e7420646f6573206e6f7420686176604482015273329030903b30b634b2102922a1a0a82a21a4209760611b606482015260840161081b565b6001600160a01b03861660009081526006602052604090206003015460ff161515600114610f9b5760405162461bcd60e51b815260206004820152603360248201527f546865204c6f73696e67206163636f756e7420646f6573206e6f7420686176656044820152721030903b30b634b2102922a1a0a82a21a4209760691b606482015260840161081b565b610fa4876119ae565b6110165760405162461bcd60e51b815260206004820152603860248201527f5468652057696e6e696e67206163636f756e74206973206e6f7420616c6c6f7760448201527f656420746f20706c617920617420746869732074696d652e0000000000000000606482015260840161081b565b61101f866119ae565b6110915760405162461bcd60e51b815260206004820152603760248201527f546865204c6f73696e67206163636f756e74206973206e6f7420616c6c6f776560448201527f6420746f20706c617920617420746869732074696d652e000000000000000000606482015260840161081b565b6001600160a01b03808816600081815260066020526040808220600c808201805460ff19908116909155958c1684529183209091018054909416909355908152815460019291906110e39084906121af565b90915550506001600160a01b03808716600090815260066020526040808220829055918916815290812060019081018054919290916111239084906121af565b90915550506001600160a01b038616600090815260066020526040812060019081018054919290916111569084906121af565b90915550506001600160a01b038088166000908152600660205260408082206003908101805464ff000000001990811664010000000017909155938a168352912001805490911690556111a98786611a4e565b6111b38685611a4e565b82156111f9576005546001600160a01b038816600090815260066020526040902054106111f95760006111e6888461077b565b90506111f28888611bb9565b9050611207565b6112038787611bb9565b5060005b9695505050505050565b6000662386f26fc10000670de0b6b3a76400008261122d61124c565b90508061123a838561223f565b6112449190612274565b935050505090565b600080600260009054906101000a90046001600160a01b03166001600160a01b031663feaf968c6040518163ffffffff1660e01b815260040160a060405180830381865afa1580156112a2573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906112c691906122a2565b505050915050806402540be4006112dd91906122f2565b91505090565b60008160000361130f57506001600160a01b03821660009081526006602052604090206004015461087b565b8160010361133957506001600160a01b03821660009081526006602052604090206005015461087b565b8160020361136457506001600160a01b0382166000908152600660208190526040909120015461087b565b8160030361138e57506001600160a01b03821660009081526006602052604090206007015461087b565b816004036113b857506001600160a01b03821660009081526006602052604090206008015461087b565b816005036113e257506001600160a01b03821660009081526006602052604090206009015461087b565b8160060361140c57506001600160a01b0382166000908152600660205260409020600a015461087b565b8160070361087b57506001600160a01b0382166000908152600660205260409020600b015461087b565b6008818154811061144657600080fd5b6000918252602090912001546001600160a01b0316905081565b60006003805461146f90612377565b80601f016020809104026020016040519081016040528092919081815260200182805461149b90612377565b80156114e85780601f106114bd576101008083540402835291602001916114e8565b820191906000526020600020905b8154815290600101906020018083116114cb57829003601f168201915b505050505090506114f98282610b96565b6115455760405162461bcd60e51b815260206004820152601f60248201527f54686973206973206e6f7420612076616c6964207472616e73616374696f6e00604482015260640161081b565b6001600160a01b0383166000908152600660205260408120908155600301805463ff00ffff1916630100010017905561157c611211565b6001600160a01b038416600090815260066020819052604082206004810193909355600583018290558201819055600782018190556008820181905560098201819055600a82018190556003909101805460ff60301b191690556115df84610c00565b6001600160a01b03909416600090815260076020526040902093909355505050565b60606040518060600160405280602281526020016123c660229139905090565b6000546001600160a01b0316331461167b5760405162461bcd60e51b815260206004820181905260248201527f4f776e61626c653a2063616c6c6572206973206e6f7420746865206f776e6572604482015260640161081b565b6001600160a01b0381166116e05760405162461bcd60e51b815260206004820152602660248201527f4f776e61626c653a206e6577206f776e657220697320746865207a65726f206160448201526564647265737360d01b606482015260840161081b565b6116e98161195e565b50565b6000600480546116fb90612377565b80601f016020809104026020016040519081016040528092919081815260200182805461172790612377565b80156117745780601f1061174957610100808354040283529160200191611774565b820191906000526020600020905b81548152906001019060200180831161175757829003601f168201915b5050505050905061178484610c5a565b15156001146117d55760405162461bcd60e51b815260206004820152601f60248201527f54686973206163636f756e74206973206e6f7420726567697374657265642e00604482015260640161081b565b6117de84610881565b151560011461182f5760405162461bcd60e51b815260206004820152601b60248201527f54686973206163636f756e74206973206e6f74206163746976652e0000000000604482015260640161081b565b6118398382610b96565b6118855760405162461bcd60e51b815260206004820152601f60248201527f54686973206973206e6f7420612076616c6964207472616e73616374696f6e00604482015260640161081b565b61188e846119ae565b15156001146118f95760405162461bcd60e51b815260206004820152603160248201527f54686973206163636f756e74206973206e6f7420616c6c6f77656420746f20706044820152703630bc9030ba103a3434b9903a34b6b29760791b606482015260840161081b565b506001600160a01b03909216600090815260066020526040902060038101805460059092019390935567ff000000000000ff191660011790915550565b60008061194a83662386f26fc1000061223f565b90506119568185612274565b949350505050565b600080546001600160a01b038381166001600160a01b0319831681178455604051919092169283917f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e09190a35050565b6001600160a01b038116600090815260066020526040812060030154600190600160301b900460ff166119e45750600192915050565b6001600160a01b038316600090815260066020526040902060020154611a0b9082906121af565b4210611a455750506001600160a01b0316600090815260066020526040812060038101805460ff60301b1916905560019081019190915590565b50600092915050565b6001600160a01b03821660009081526006602052604081206001810154600390910154909190600160381b900460ff16611b53576006821015611a9d57611a966001836121dd565b9050611b19565b6009821115611aec57611ab16005836123b1565b600003611ae157506001600160a01b0383166000908152600660205260408120600301805460ff19169055611b19565b611a966001826121af565b6001600160a01b0384166000908152600660205260409020600301805460ff60381b1916600160381b1790555b6001600160a01b038416600090815260066020526040902060030154600160381b900460ff16611b4e57611b4e848483611c6c565b610b90565b6001600160a01b0384166000908152600660205260409020600190810154600591611b7e91906121af565b611b8891906123b1565b600003610b90575050506001600160a01b03166000908152600660205260409020600301805460ff60381b19169055565b6001600160a01b038216600090815260066020526040902060010154606403611c11576001600160a01b038216600090815260066020526040902060038101805460ff60301b1916600160301b179055426002909101555b6001600160a01b038116600090815260066020526040902060010154606403610ab7576001600160a01b038116600090815260066020526040902060038101805460ff60301b1916600160301b179055426002909101555050565b80600003611c98576001600160a01b038316600090815260066020819052604090912001829055611d40565b80600103611cc3576001600160a01b0383166000908152600660205260409020600701829055611d40565b80600203611cee576001600160a01b0383166000908152600660205260409020600801829055611d40565b80600303611d19576001600160a01b0383166000908152600660205260409020600901829055611d40565b80600403611d40576001600160a01b0383166000908152600660205260409020600a018290555b6001600160a01b0383166000908152600660208190526040909120600a8101546009820154600883015460078401549390940154919390929091611d8491906121af565b611d8e91906121af565b611d9891906121af565b611da291906121af565b6001600160a01b039093166000908152600660205260409020600b8101939093555050600c01805460ff19166001179055565b80356001600160a01b0381168114611dec57600080fd5b919050565b60008060408385031215611e0457600080fd5b611e0d83611dd5565b946020939093013593505050565b600060208284031215611e2d57600080fd5b611e3682611dd5565b9392505050565b634e487b7160e01b600052604160045260246000fd5b604051601f8201601f1916810167ffffffffffffffff81118282101715611e7c57611e7c611e3d565b604052919050565b60006020808385031215611e9757600080fd5b823567ffffffffffffffff80821115611eaf57600080fd5b818501915085601f830112611ec357600080fd5b813581811115611ed557611ed5611e3d565b8060051b9150611ee6848301611e53565b8181529183018401918481019088841115611f0057600080fd5b938501935b83851015611f2557611f1685611dd5565b82529385019390850190611f05565b98975050505050505050565b600082601f830112611f4257600080fd5b813567ffffffffffffffff811115611f5c57611f5c611e3d565b611f6f601f8201601f1916602001611e53565b818152846020838601011115611f8457600080fd5b816020850160208301376000918101602001919091529392505050565b60008060408385031215611fb457600080fd5b823567ffffffffffffffff80821115611fcc57600080fd5b611fd886838701611f31565b93506020850135915080821115611fee57600080fd5b50611ffb85828601611f31565b9150509250929050565b60008060008060008060c0878903121561201e57600080fd5b61202787611dd5565b955061203560208801611dd5565b945060408701359350606087013592506080870135801515811461205857600080fd5b8092505060a087013590509295509295509295565b60006020828403121561207f57600080fd5b5035919050565b6000806040838503121561209957600080fd5b6120a283611dd5565b9150602083013567ffffffffffffffff8111156120be57600080fd5b611ffb85828601611f31565b60005b838110156120e55781810151838201526020016120cd565b83811115610b905750506000910152565b60208152600082518060208401526121158160408501602087016120ca565b601f01601f19169190910160400192915050565b60008060006060848603121561213e57600080fd5b61214784611dd5565b9250602084013567ffffffffffffffff81111561216357600080fd5b61216f86828701611f31565b925050604084013590509250925092565b60006020828403121561219257600080fd5b5051919050565b634e487b7160e01b600052601160045260246000fd5b600082198211156121c2576121c2612199565b500190565b634e487b7160e01b600052603260045260246000fd5b6000828210156121ef576121ef612199565b500390565b634e487b7160e01b600052603160045260246000fd5b60006001820161221c5761221c612199565b5060010190565b600082516122358184602087016120ca565b9190910192915050565b600081600019048311821515161561225957612259612199565b500290565b634e487b7160e01b600052601260045260246000fd5b6000826122835761228361225e565b500490565b805169ffffffffffffffffffff81168114611dec57600080fd5b600080600080600060a086880312156122ba57600080fd5b6122c386612288565b94506020860151935060408601519250606086015191506122e660808701612288565b90509295509295909350565b60006001600160ff1b038184138284138082168684048611161561231857612318612199565b600160ff1b600087128281168783058912161561233757612337612199565b6000871292508782058712848416161561235357612353612199565b8785058712818416161561236957612369612199565b505050929093029392505050565b600181811c9082168061238b57607f821691505b6020821081036123ab57634e487b7160e01b600052602260045260246000fd5b50919050565b6000826123c0576123c061225e565b50069056fe54484520544553542046554e4354494f4e20495320574f524b494e47212121212121a264697066735822122009af4a4535d39a302531dfd56630e78fc44de713c6d5fdbe9e6b5258d4e9a88c64736f6c634300080e0033"

@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            if type(user) == str:
                data["error"] = user
                data["isErr"] = True
                return Response(data)
            data['response'] = "succesfully registered a new user."
            data['username'] = user.username
            user1 = User.objects.get(username=data['username'])
            token = user1.token
            data['token'] = token.token
            user1.in_game = False
            user1.in_queue = False
            user1.logged_in = True
            if request.data['phone_number'] != "":
                user1.phone_number = request.data['phone_number']
                user1.has_phone_number = True
            user1.save()
        else:
            data = serializer.errors
        return Response(data)

@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)

    data = {}
    if serializer.is_valid():
        user = serializer.save()
        if type(user) == dict:
            return Response(user)
        data['response'] = "Success"
        data['username'] = user.username
        user1 = User.objects.get(username=user.username)
        if user1.logged_in:
            newData = {
                'log_in_error': "User already logged in."
            }
            return Response(newData)
        user1.in_game = False
        user1.in_queue = False
        user1.logged_in = True
        user1.save()
        token = binascii.hexlify(os.urandom(config('TOKEN', cast=int))).decode()
        token1 = user1.token
        token1.token = token
        token1.save()
        data['token'] = token
    else:
        data = serializer.errors
    return Response(data)

@api_view(['POST'])
def get_user(request):
    print("IN GET USER")
    newData = {
        "token": request.data['token']
    }
    print(newData)
    de_queue = request.data['de_queue']
    
    serializer = GetUserSerializer(data=newData)

    data = {}

    if serializer.is_valid():
        print("SERIALIZER VALID")
        user = serializer.save()
        data['response'] = "Getting your information"
        data['username'] = user.username
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        try:
            print("IN TRY BLOCK")
            data['wins'] = user.wins
            data['losses'] = user.losses
            data['best_streak'] = user.best_streak
            data['win_streak'] = user.win_streak
        except:
            print("IN EXCEPT BLOCK")
            pass
        if type(user.friends) == list:
            print("USER HAS FRIENDS")
            data['friends'] = user.friends
        else:
            print("USER HAS 0 FRIENDS")
            data['friends'] = ["0"]
        hasInvites = False
        invites = []
        for invite in GameInvite.objects.all():
            if invite.reciever == user.username:
                print("USER HAS INVITES")
                hasInvites = True
                invites.append(invite.sender)
        data['hasInvite'] = hasInvites
        data['invites'] = invites
        data['is_guest'] = user.is_guest
        if user.phone_number:
            print("USER HAS PHONE NUMBER")
            data['phone_number'] = user.phone_number
            user.has_phone_number = True
            data['HPN'] = True
            user.save()
        else:
            print("USER HAS NO PHONE NUMBER")
            data['phone_number'] = "No Phone number"
            data['HPN'] = False
    else: 
        print("SERIALIZER ERRORS")
        data = serializer.errors
    print("DATA BELOW")
    print(data)
    if de_queue:
        user.in_queue = False
        user.in_game = False
        user.save()
    return Response(data)

@api_view(['POST'])
def logout_view(request):
    session = request.data['token']
    
    data = {}

    token1 = None
    try:
        for token in Token.objects.all():
            if token.token == session:
                token1 = token
        data['response'] = "Success"
    except:
        data['response'] = "Failure"
        return Response(data)
    user = User.objects.get(token=token1)
    if user.is_guest:
        token1.delete()
        user.delete()
    else:
        user.logged_in = False
        user.in_queue = False
        user.in_game = False
        user.save()
        token1.token = "null"
        token1.save()
    return Response(data)

@api_view(['POST'])
def send_points(request):
    print("***** IN SEND POINTS *****")
    _winner = None
    _loser = None
    if request.data['type'] == "Custom":
        data = {
            "gameOver" : True
        }
        return Response(data)

    if request.data['winner'] == False:
        data = {
            "gameOver" : True
        }
        return Response(data)

    fPoints = request.data['fPoints']
    sPoints = request.data['sPoints']
    gameId = request.data['gameId']
    game = Game.objects.get(gameId=gameId)
    user1 = User.objects.get(username=game.first)
    user2 = User.objects.get(username=game.second)
    right_now = make_aware(datetime.datetime.now())
    
    if fPoints > sPoints:
        print("***** FPOINTS IS GREATER *****")
        user1.wins += 1
        _winner = user1
        _loser = user2

        if user1.streak_time:
            print("USER 1 HAS A STREAK TIME")
            time_limit = user1.streak_time + timedelta(minutes=2)
            if right_now < time_limit:
                print("STILL WITHIN THE TIME LIMITS")
                user1.win_streak += 1
            else:
                print("NOT WITHIN THE TIME LIMITS")
                user1.win_streak = 1
        else:
            print("NO STREAK TIME")
            user1.win_streak = 1 

        if user1.win_streak > user1.best_streak:
            print("NEW BEST STREAK")
            user1.best_streak = user1.win_streak

        user1.streak_time = right_now
        user1.save()
        user2.losses += 1
        if user2.win_streak > user2.best_streak:
            user2.best_streak = user2.win_streak
        user2.win_streak = 0
        user2.save()
        game.fPoints = fPoints
        game.sPoints = sPoints
        game.winner = user1.username
        game.winner_streak = user1.win_streak
        game.save()
    elif sPoints > fPoints:
        print("***** SPOINTS IS GREATER *****")
        user1.losses += 1
        _winner = user2
        _loser = user1
        if user1.win_streak > user1.best_streak:
            user1.best_streak = user1.win_streak
        user1.win_streak = 0
        user1.save()
        user2.wins += 1
        if user2.streak_time:
            print("USER 2 HAS A STREAK TIME")
            time_limit = user2.streak_time + timedelta(minutes=2)
            if right_now < time_limit:
                print("STILL WITHIN THE TIME LIMITS")
                user2.win_streak += 1
            else:
                print("NOT WITHIN TIME LIMITS")
                user2.win_streak = 1
        else:
            print("NO STREAK TIME")
            user2.win_streak = 1
        if user2.win_streak > user2.best_streak:
            print("NEW BEST STREAK")
            user2.best_streak = user2.win_streak
        user2.streak_time = right_now
        user2.save()
        game.fPoints = fPoints
        game.sPoints = sPoints
        game.winner = user2.username
        game.winner_streak = user2.win_streak
        game.save()
    else:
        print("***** IT IS A TIE *****")
        print("STOP")
        game.fPoints = fPoints
        game.sPoints = sPoints
        game.winner = "Tie"
        game.winner_streak = 0
        game.save()
    
    contract_address = config('CONTRACT_ADDRESS')  # Replace with your contract address
    contract_abi = contract_abi_const
    print("SET THE CONTRACT ADDRRESS AND ABI")
    tapcoingame = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    print("CALLING THE TAPCOINS GAM FUNCTION BELOW")
    functionCall = tapcoingame.functions.updatePlayersWins(_winner.dev_ganache_wallet_address, 
                                                           _loser.dev_ganache_wallet_address,
                                                           1000,
                                                           1000,
                                                           False,
                                                           70).call()
    print(functionCall)
    print("THE CALL DATA SHOULD BE ABOVE")

    data = {
        "gameOver" : True
    }

    return Response(data)

@api_view(['POST'])
def create_game(request):
    
    token = Token.objects.get(token=request.data['token'])
    token1 = Token.objects.get(token=request.data['first'])
    token2 = Token.objects.get(token=request.data['second'])
    user = User.objects.get(token=token)
    user1 = User.objects.get(token=token1)
    user2 = User.objects.get(token=token2)

    data = {}

    if user.in_game == False:
        gameId = binascii.hexlify(os.urandom(8)).decode()
        Game.objects.create(first=user1.username, second=user2.username, gameId=gameId)
        user1.cg_Id = gameId
        user2.cg_Id = gameId
        user1.in_game = True
        user2.in_game = True
        user1.save()
        user2.save()
        data['gameId'] = gameId
        data['first'] = "True"
    else:
        data['gameId'] = user2.cg_Id
        data['first'] = "False"
        user1.in_game = False
        user2.in_game = False
        user1.save()
        user2.save()

    return Response(data)

@api_view(['POST'])
def guest_login(request):
    data = {}
    token = binascii.hexlify(os.urandom(config('TOKEN', cast=int))).decode()
    pw = "guestPassword"
    salt = bcrypt.gensalt(rounds=config('ROUNDS', cast=int))
    hashed = bcrypt.hashpw(pw.encode(config('ENCODE')), salt).decode()
    token1 = Token.objects.create(token=token)
    count = 0
    for user in User.objects.all():
        try:
            if user.username.split("_")[0] == "CoinTapper":
                count += 1
        except:
            count = count

    newCount = str(count)
    user = None
    try:
        user = User.objects.create(first_name="Guest",last_name="Tapper", username="CoinTapper_" + newCount, token=token1, password=hashed)
        user.is_guest = True
        user.in_game = False
        user.in_queue = False
        user.logged_in = True
        user.save()
        data['response'] = "succesfully registered a new guest user."
        data['username'] = user.username
        data['error'] = False
        data['token'] = token1.token
    except Exception as e:
        newError = str(e)
        newErr = newError.split("DETAIL:")[1]
        error = newErr.split("=")[1]
        data['response'] = "Something went wrong."
        data['username'] = error
        data['error'] = True
        data['token'] = ""
        return Response(data)

    return Response(data)

@api_view(['POST'])
def send_cb(request):
    tToken = request.data['token']
    token = Token.objects.get(token=tToken)
    user = User.objects.get(token=token)

    CommentOrBug.objects.create(message=request.data['text'], user=user.username)

    data={
        'response':'Successfully Sent'
    }

    return Response(data)

@api_view(['POST'])
def check_in_game(request):

    tk = request.data['token']
    token = Token.objects.get(token=tk)
    user = User.objects.get(token=token)
    data = {}
    if user.in_game:
        data['response'] = "INGAME"
    else:
        data['response'] = "OUTGAME"

    return Response(data)

@api_view(['POST'])
def send_friendRequest(request):
    try:
        token1 = Token.objects.get(token=request.data['token'])
        user1 = User.objects.get(token=token1)
        user2 = User.objects.get(username=request.data['username'])
        if user1 == user2:
            data = {
                "result": "Cannot send request to self.",
                "friends": ["No friends"]
            }
            return Response(data)
        rString = "requested|"
        sString = "sentTo|"
        fRequest = rString + user1.username
        sRequest = sString + user2.username
        for friend in user1.friends:
            if sString in friend:
                if friend.split(sString)[1] == user2.username:
                    data = {
                        "result": "ALREADY SENT TO",
                        "friends": [user2.username]
                    }
                    return Response(data)
            elif rString in friend:
                if friend.split(rString)[1] == user2.username:
                    data = {
                        "result": "ALREADY RECIEVED",
                        "friends": [user2.username]
                    }
                    return Response(data)
        tempFriends1 = []
        tempFriends2 = []
        if type(user2.friends) == list:
            for name in user2.friends:
                if name != fRequest:
                    if name != sRequest:
                        tempFriends1.append(name)
        tempFriends1.append(fRequest)
        if type(user1.friends) == list:
            for name in user1.friends:
                if name != fRequest:
                    if name != sRequest:
                        tempFriends2.append(name)
        tempFriends2.append(sRequest)
        user1.friends = tempFriends2
        user2.friends = tempFriends1
        user1.save()
        user2.save()
        data = {
            "result": "Success",
            "friends": user1.friends
        }
        return Response(data)
    except:
        data = {
            "result": "Could not find username.",
            "friends": ["No friends"]
        }
        return Response(data)

@api_view(['POST'])
def accept_friendRequest(request):
    try:
        token1 = Token.objects.get(token=request.data['token'])
        accepter = User.objects.get(token=token1)
        sender = User.objects.get(username=request.data['username'])
        rString = "requested|"
        sString = "sentTo|"
        newFriends = []
        for name in accepter.friends:
            if rString in name:
                newName = name.split("|")[1]
                if newName == sender.username:
                    newFriends.append(newName)
                else:
                    newFriends.append(name)
            else:
                newFriends.append(name)
        accepter.friends = newFriends
        accepter.save()
        newFriends2 = []
        for name in sender.friends:
            if sString in name:
                newName = name.split("|")[1]
                if newName == accepter.username:
                    newFriends2.append(newName)
                else:
                    newFriends2.append(name)
            else:
                newFriends2.append(name)
        sender.friends = newFriends2
        sender.save()
        data = {
            "result": "Accepted"
        }
        return Response(data)
    except:
        data = {
            "result": "Colud not accept request"
        }
        return Response(data)

@api_view(['POST'])
def decline_friendRequest(request):
    try:
        token1 = Token.objects.get(token=request.data['token'])
        decliner = User.objects.get(token=token1)
        sender = User.objects.get(username=request.data['username'])
        rString = "requested|"
        sString = "sentTo|"
        newFriends = []
        for name in decliner.friends:
            if rString in name:
                newName = name.split("|")[1]
                if newName != sender.username:
                    newFriends.append(name)
            else:
                newFriends.append(name)
        decliner.friends = newFriends
        decliner.save()
        newFriends2 = []
        for name in sender.friends:
            if sString in name:
                newName = name.split("|")[1]
                if newName != decliner.username:
                    newFriends2.append(name)
            else:
                newFriends2.append(name)
        sender.friends = newFriends2
        sender.save()
        data = {
            "result": "Declined"
        }
        return Response(data)
    except:
        data = {
            "result": "Colud not decline request."
        }
        return Response(data)

@api_view(['POST'])
def remove_friend(request):
    try:
        token1 = Token.objects.get(token=request.data['token'])
        remover = User.objects.get(token=token1)
        removed = User.objects.get(username=request.data['username'])
        newFriends = []
        for name in remover.friends:
            if name != removed.username:
                newFriends.append(name)
        remover.friends = newFriends
        remover.save()
        newFriends2 = []
        for name in removed.friends:
            if name != remover.username:
                newFriends2.append(name)
        removed.friends = newFriends2
        removed.save()
        data = {
            "result": "Removed"
        }
        return Response(data)
    except:
        data = {
            "result": "Could not remove friend."
        }
        return Response(data)

@api_view(['POST'])
def send_invite(request):
    token = Token.objects.get(token=request.data['token'])
    user1 = User.objects.get(token=token)
    user2 = User.objects.get(username=request.data['username'])
    gameId = binascii.hexlify(os.urandom(8)).decode()
    uniqueId = False
    while(not uniqueId):
        foundId = False
        for game in Game.objects.all():
            if game.gameId == gameId:
                foundId = True
                break
        if foundId:
            gameId = binascii.hexlify(os.urandom(8)).decode()
        else:
            uniqueId = True
    for gInvite in GameInvite.objects.all():
        if gInvite.sender == user1.username:
            if gInvite.reciever == user2.username:
                data = {
                    "first": "ALREADY EXISTS",
                    "second": "ALREADY EXISTS",
                    "gameId": "ALREADY EXISTS"
                }
                return Response(data)
        elif gInvite.sender == user2.username:
            if gInvite.reciever == user1.username:
                data = {
                    "first": "ALREADY EXISTS",
                    "second": "ALREADY EXISTS",
                    "gameId": "ALREADY EXISTS"
                }
                return Response(data)
    GameInvite.objects.create(sender=user1.username, reciever=user2.username, gameId=gameId)
    Game.objects.create(first=user1.username, second=user2.username, gameId=gameId)
    data = {
        "first":user1.username,
        "second":user2.username,
        "gameId":gameId
    }
    return Response(data)

@api_view(['POST'])
def ad_invite(request):
    sender = User.objects.get(username=request.data['username'])
    token = Token.objects.get(token=request.data['token'])
    reciever = User.objects.get(token=token)
    ad_request = request.data['adRequest']
    try:
        if ad_request == "delete":
            deleted = False
            try:
                if request.data['cancelled'] == True:
                    data = {
                        "result": "Cancelled"
                    }
                    return Response(data)
                else:
                    for invite in GameInvite.objects.all():
                        if invite.sender == sender.username:
                            if invite.reciever == reciever.username:
                                game = Game.objects.get(gameId=invite.gameId)
                                game.delete()
                                invite.delete()
                                deleted = True
                        elif invite.sender == reciever.username:
                            if invite.reciever == sender.username:
                                game = Game.objects.get(gameId=invite.gameId)
                                game.delete()
                                invite.delete()
                                deleted = True
                    if deleted:
                        data = {
                            "result": "Cancelled"
                        }
                    else:
                        data = {
                            "result": "Soemthing went wrong"
                        }
                    return Response(data)
            except:
                for invite in GameInvite.objects.all():
                    if invite.sender == sender.username:
                        if invite.reciever == reciever.username:
                            game = Game.objects.get(gameId=invite.gameId)
                            game.delete()
                            invite.delete()
                            deleted = True
                    elif invite.sender == reciever.username:
                        if invite.reciever == sender.username:
                            game = Game.objects.get(gameId=invite.gameId)
                            game.delete()
                            invite.delete()
                            deleted = True
                if deleted:
                    data = {
                        "result": "Cancelled"
                    }
                else:
                    data = {
                        "result": "Soemthing went wrong"
                    }
                return Response(data)
        else:
            game = None
            for invite in GameInvite.objects.all():
                if invite.sender == sender.username:
                    if invite.reciever == reciever.username:
                        game = Game.objects.get(gameId=invite.gameId)
                        invite.delete()
                        deleted = True
                elif invite.sender == reciever.username:
                    if invite.reciever == sender.username:
                        game = Game.objects.get(gameId=invite.gameId)
                        invite.delete()
                        deleted = True
            if deleted:
                data = {
                    "result": "Accepted",
                    "first":game.first,
                    "second":game.second,
                    "gameId":game.gameId
                }
            else:
                data = {
                    "result": "Soemthing went wrong"
                }
            return Response(data)
    except:
        data = {
            "result": "Somethiong went wrong"
        }
        return Response(data)

@api_view(['POST'])
def send_username(request):
    phone_number = request.data['phone_number']
    data = {
        "response": True,
        "message" : ""
    }

    try:
        user = User.objects.get(phone_number=phone_number)
        data['message'] = "BEFORE SEND TEXT"
        requests.post('https://textbelt.com/text', {
            'phone': phone_number,
            'message': f'Your username is: {user.username}',
            'key': '0d40a9c1f04d558428eb525db9b4502e0a15cd31F5JAs5vP0Yc2JcS2TzrtsqFKd',
        })
        data['message'] = "RESPONSE IS A SUCCESS"
    except Exception as e:
        data['response'] = False
        data['message'] = f"IN THE EXCEPT BLOCK e: {e}"
    
    return Response(data)

@api_view(['POST'])
def send_code(request):
    phone_number = request.data['phone_number']
    code = ""

    for i in range(4):
        num = randrange(10)
        code += str(num)
    data = {
        "response": True,
        "code" : code
    }

    try:
        user = User.objects.get(phone_number=phone_number)
        data['message'] = "BEFORE SEND TEXT"
        requests.post('https://textbelt.com/text', {
            'phone': phone_number,
            'message': f'Your temporary code is: {code}',
            'key': '951292afc50e335e0bc2ac92e70e3ecd4030853aQFJFjuPmMccnZjNCihpssKcII',
        })
        right_now = make_aware(datetime.datetime.now())
        user.p_code = int(code)
        user.p_code_time = right_now
        user.save()
        data['message'] = f"RESPONSE IS A SUCCESS {right_now}."
    except Exception as e:
        data['response'] = False
        data['message'] = f"IN THE EXCEPT BLOCK e: {e}"
    
    return Response(data)

@api_view(['POST'])
def change_password(request):
    if request.data['code'] == "SAVE":
        print("IN SAVED IF STATMENT")
        data = {
            "response": True,
            "message": "",
            "error_type": 0
        }
        try:
            print("IN THE TRY BLOCK")
            password = request.data['password']
            if password.strip() == "":
                data["response"] = False
                data["error_type"] = 0
                data["message"] = "Password can't be blank."
                return Response(data)
            print("AFTER CHECKING FOR EMPTY")
            token = Token.objects.get(token=request.data['token'])
            user = User.objects.get(token=token)
            print("GOT USER")
            newPW = bcrypt.hashpw(password.encode(config('ENCODE')), user.password.encode(config('ENCODE')))
            print("GOT NEW PW")
            if newPW == user.password.encode(config('ENCODE')):
                print("PASSWORD IS PREVIOUS PASSWORD")
                data["response"] = False
                data["error_type"] = 1
                data["message"] = "Password can't be previous password."
                print(data)
                return Response(data)
            print("PASSWORDS ARE DIFFERENT")
            salt = bcrypt.gensalt(rounds=config('ROUNDS', cast=int))
            print("GOT THE SALT")
            hashed = bcrypt.hashpw(password.encode(config('ENCODE')), salt).decode()
            print("GOT THE HASHED")
            user.password = hashed
            print("SET USER PASSWORD")
            user.is_guest = False
            print("SET THE GUEST")
            user.save()
        except:
            print("IN EXCEPT BLOCK")
            data["response"] = False
            data["error_type"] = 3
            data["message"] = "Something went wrong."
        return Response(data)

    data = {
        "response": True,
        "expired": False,
        "message": "",
        "error_type": 0
    }
    code = request.data['code']
    password = request.data['password']
    if password.strip() == "":
        data["response"] = False
        data["error_type"] = 0
        data["message"] = "Password can't be blank."
        data["expired"] = False
        return Response(data)
    user = User.objects.get(p_code=int(code))
    ser_data = {
        "username": user.username,
        "password": password
    }
    newPW = bcrypt.hashpw(password.encode(config('ENCODE')), user.password.encode(config('ENCODE')))
    if newPW == user.password.encode(config('ENCODE')):
        data["response"] = False
        data["error_type"] = 1
        data["message"] = "Password can't be previous password."
        data["expired"] = False
        return Response(data)
    p_word_datetime_limit = user.p_code_time + timedelta(minutes=5)
    right_now = make_aware(datetime.datetime.now())
    try:
        if p_word_datetime_limit > right_now:
            salt = bcrypt.gensalt(rounds=config('ROUNDS', cast=int))
            hashed = bcrypt.hashpw(password.encode(config('ENCODE')), salt).decode()
            user.password = hashed
            user.save()
            data['message'] = f"Successfully saved password."
        else:
            data["response"] = False
            data['message'] = "Time limit reached. Invalid code."
            data["error_type"] = 2
            data['expired'] = True
    except:
        data['response'] = False
        data["error_type"] = 3
        data['message'] = "Something went wrong."
        data['expired'] = False

    return Response(data)
        
@api_view(['POST'])
def save(request):
    print("IN SAVE")
    data = {
        "response" : ""
    }

    try:
        print("IN TRY BLOCK")
        token = Token.objects.get(token=request.data['token'])
        print("CREATED TOKEN")
        user = User.objects.get(token=token)
        print("FOUND USER")
        for u in User.objects.all():
            if u.username == request.data['username']:
                if u != user:
                    print("INVALID USERNAME")
                    data['response'] = "Invalid username."
                    return Response(data)
        print("SAVING DATA")
        user.first_name = request.data['first_name']
        print("SAVED FIRST NAME")
        user.last_name = request.data['last_name']
        print("SAVED LAST NAME")
        user.username = request.data['username']
        print("SAVED USERNAME")
        user.phone_number = request.data['phone_number']
        print("SAVED PHONE NUMBER")
        user.save()
        print("SAVED")
        if request.data['guest']:
            print("IS A GUEST")
            data['response'] = "Guest"
        else:
            print("IS NOT A GUEST")
            data['response'] = "Successfully saved data."
    except Exception as e:
        print("E IS BELOW")
        print(e)
        data['response'] = "Something went wrong: " + e

    return Response(data)

@api_view(['POST'])
def save_wallet(request):
    try:
        if config('DEBUG', cast=bool) == True:
            token = request.data['wallet']
            get_user_data = {
                "token": token
            }
            serializer = GetUserSerializer(data=get_user_data)

            if serializer.is_valid():
                print("GOT THE USER THROUGH SERIALIZER")
                user = serializer.save()
                adding_wallet = user.dev_ganache_wallet_address
                print("ADDING WALLET BELOW")
                print(adding_wallet)
                # Load the contract ABI and address
                contract_address = config('CONTRACT_ADDRESS')  # Replace with your contract address
                contract_abi = contract_abi_const
                print("SET THE CONTRACT ADDRRESS AND ABI")
                tapcoingame = w3.eth.contract(
                    address=contract_address,
                    abi=contract_abi
                )

                function_to_call = tapcoingame.functions.addWallet(user.dev_ganache_wallet_address, "TEMPORARYADDWALLETPASSCODE")

                # Build the transaction
                transaction = function_to_call.buildTransaction({
                    "chainId": 1337,  # Replace with the appropriate chain ID
                    "gasPrice": 20000000000,  # Set the gas price as needed
                    "gas": 6721975,  # Set the gas limit as needed
                    "nonce": w3.eth.getTransactionCount(w3.eth.accounts[1]),
                })

                # Sign the transaction
                signed_transaction = w3.eth.account.signTransaction(transaction, "f346cd0113bc66130355e338c12d0bc24aca0e13da4f520a7ce6be94d319fead")

                # Send the transaction
                transaction_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

                # Print the transaction hash
                print("Transaction Hash:", transaction_hash)

                # Mine a specified number of blocks to include the transaction
                blocks_to_mine = 1  # Adjust this value as needed
                for _ in range(blocks_to_mine):
                    response = requests.post(ganache_rpc_url, json={
                        "jsonrpc": "2.0",
                        "method": "evm_mine",
                        "params": [],
                        "id": 1
                    })
                    response.raise_for_status()
                    print(f"Mined block {w3.eth.blockNumber}")

                # Check the transaction status
                receipt = w3.eth.waitForTransactionReceipt(transaction_hash)
                print("Transaction Status:", receipt["status"])

                # Works but without persisting data
                # print("CALLING THE TAPCOINS GAM FUNCTION BELOW")
                # functionCall = tapcoingame.functions.addWallet(user.dev_ganache_wallet_address, "TEMPORARYADDWALLETPASSCODE").call()
                # print(functionCall)
                # print("THE CALL DATA SHOULD BE ABOVE")
                data = {
                    "response": user.dev_ganache_wallet_address
                }
                return Response(data)
            else:
                print("SERIALIZER IS IN VALID")
                data = {
                    "response": "Something went wrong."
                }
                return Response(data)
        else:
            wallet_address = request.data['wallet']
            if wallet_address != "None":
                print("THE WALLET ADDRESS IS BELOW")
                print(wallet_address)
                # Load the contract ABI and address
                contract_address = config('CONTRACT_ADDRESS')  # Replace with your contract address
                contract_abi = contract_abi_const
                print("SET THE CONTRACT ADDRRESS AND ABI")

                # Create a contract object
                contract = w3.eth.contract(address=contract_address, abi=contract_abi)
                print("CREATED THE CONTRACT VARIABLE")

                # Interact with the contract (e.g., call functions)
                result = contract.functions.addWallet(wallet_address, "TEMPORARYADDWALLETPASSCODE").call()
                print("RESULT IS BELOW")
                print(result)
                data = {
                    "response": "SUCCESS"
                }
                return Response(data)
       
    except Exception as e:
        print("IN THE EXCEPT BLOCK")
        print(e)
        data = {
            "response": "Something went wrong."
        }
        return Response(data)

@api_view(['POST'])
def pass_face_id(request):
    try:
        if config('DEBUG', cast=bool) == True:
            token = request.data['token']
            get_user_data = {
                "token": token
            }
            serializer = GetUserSerializer(data=get_user_data)

            if serializer.is_valid():
                print("GOT THE USER THROUGH SERIALIZER")
                user = serializer.save()
                # Load the contract ABI and address
                contract_address = config('CONTRACT_ADDRESS')  # Replace with your contract address
                contract_abi = contract_abi_const
                print("SET THE CONTRACT ADDRRESS AND ABI")
                tapcoingame = w3.eth.contract(
                    address=contract_address,
                    abi=contract_abi
                )
                
                # function_to_call = tapcoingame.functions.faceIdCheck("0x8BF1f83632e48CcB24A777706FCD27ee16456107", "TEMPORARYFACEIDCODE", 10000)

                # # Build the transaction
                # transaction = function_to_call.buildTransaction({
                #     "chainId": 1337,  # Replace with the appropriate chain ID
                #     "gasPrice": 20000000000,  # Set the gas price as needed
                #     "gas": 6721975,  # Set the gas limit as needed
                #     "nonce": w3.eth.getTransactionCount(w3.eth.accounts[1]),
                # })

                # # Sign the transaction
                # signed_transaction = w3.eth.account.signTransaction(transaction, "f346cd0113bc66130355e338c12d0bc24aca0e13da4f520a7ce6be94d319fead")

                # # Send the transaction
                # transaction_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

                # # Print the transaction hash
                # print("Transaction Hash:", transaction_hash)

                # # Mine a specified number of blocks to include the transaction
                # blocks_to_mine = 1  # Adjust this value as needed
                # for _ in range(blocks_to_mine):
                #     response = requests.post(ganache_rpc_url, json={
                #         "jsonrpc": "2.0",
                #         "method": "evm_mine",
                #         "params": [],
                #         "id": 1
                #     })
                #     response.raise_for_status()
                #     print(f"Mined block {w3.eth.blockNumber}")

                # # Check the transaction status
                # receipt = w3.eth.waitForTransactionReceipt(transaction_hash)
                # print("Transaction Status:", receipt["status"])
                
                
                print("CALLING THE TAPCOINS GAME FUNCTION BELOW")
                # functionCall = tapcoingame.functions.testFunction().call()
                functionCall = tapcoingame.functions.faceIdCheck("0x1b94A5FEe4a7727810C77198FD1bcFDdF7285bd9", "TEMPORARYFACEIDCODE", 10000).call()
                print(functionCall)
                print("THE CALL DATA SHOULD BE ABOVE")
                data = {
                    "result": "Success"
                }
                return Response(data)
            else:
                print("SERIALIZER IS IN VALID")
                data = {
                    "result": "Something went wrong."
                }
                return Response(data)
        else:
            # wallet_address = request.data['wallet']
            # if wallet_address != "None":
            #     print("THE WALLET ADDRESS IS BELOW")
            #     print(wallet_address)
            #     # Load the contract ABI and address
            #     contract_address = config('CONTRACT_ADDRESS')  # Replace with your contract address
            #     contract_abi = contract_abi_const
            #     print("SET THE CONTRACT ADDRRESS AND ABI")

            #     # Create a contract object
            #     contract = w3.eth.contract(address=contract_address, abi=contract_abi)
            #     print("CREATED THE CONTRACT VARIABLE")

            #     # Interact with the contract (e.g., call functions)
            #     result = contract.functions.addWallet(wallet_address, "TEMPORARYADDWALLETPASSCODE").call()
            #     print("RESULT IS BELOW")
            #     print(result)
            #     data = {
            #         "response": "SUCCESS"
            #     }
            #     return Response(data)
            data = {
                    "result": "NOTDEVENVIORNMENT"
                }
            return Response(data)
    except Exception as e:
        print("IN THE EXCEPT BLOCK")
        print(e)
        data = {
            "result": "Something went wrong."
        }
        return Response(data)
    
@api_view(['POST'])
def update_players_wins(request):
    try:
        if config('DEBUG', cast=bool) == True:
            # Get tokens of both users from UI later
            token = request.data['token']
            get_user_data = {
                "token": token
            }
            serializer = GetUserSerializer(data=get_user_data)

            if serializer.is_valid():
                print("GOT THE USER THROUGH SERIALIZER")
                user = serializer.save()
                # Load the contract ABI and address
                contract_address = config('CONTRACT_ADDRESS')  # Replace with your contract address
                contract_abi = contract_abi_const
                print("SET THE CONTRACT ADDRRESS AND ABI")
                tapcoingame = w3.eth.contract(
                    address=contract_address,
                    abi=contract_abi
                )
                
                function_to_call = tapcoingame.functions.updatePlayersWins("0x1b94A5FEe4a7727810C77198FD1bcFDdF7285bd9", "0x8BF1f83632e48CcB24A777706FCD27ee16456107", 10000000000000000000000000000000000, 10000000000000000000000000000000000, True, 70)

                # Build the transaction
                transaction = function_to_call.buildTransaction({
                    "chainId": 1337,  # Replace with the appropriate chain ID
                    "gasPrice": 20000000000,  # Set the gas price as needed
                    "gas": 6721975,  # Set the gas limit as needed
                    "nonce": w3.eth.getTransactionCount(w3.eth.accounts[0]),
                })

                # Sign the transaction
                signed_transaction = w3.eth.account.signTransaction(transaction, "dc0a298c4ddc2e9a5ac8725963f4f96a0cc2054a0620328b4c466f7badd44bdf")

                # Send the transaction
                transaction_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

                # Print the transaction hash
                print("Transaction Hash:", transaction_hash)

                # Mine a specified number of blocks to include the transaction
                blocks_to_mine = 1  # Adjust this value as needed
                for _ in range(blocks_to_mine):
                    response = requests.post(ganache_rpc_url, json={
                        "jsonrpc": "2.0",
                        "method": "evm_mine",
                        "params": [],
                        "id": 1
                    })
                    response.raise_for_status()
                    print(f"Mined block {w3.eth.blockNumber}")

                # Check the transaction status
                receipt = w3.eth.waitForTransactionReceipt(transaction_hash)
                print("Transaction Status:", receipt["status"])
                
                # print("CALLING THE TAPCOINS GAME FUNCTION BELOW")
                # # functionCall = tapcoingame.functions.testFunction().call()
                # functionCall = tapcoingame.functions.updatePlayersWins("0x1b94A5FEe4a7727810C77198FD1bcFDdF7285bd9", "0x8BF1f83632e48CcB24A777706FCD27ee16456107", 10000000000000000000000000000000000, 10000000000000000000000000000000000, True, 60).call()
                                                                                                                                                                                          
                # print(functionCall)
                # print("THE CALL DATA SHOULD BE ABOVE")
                data = {
                    "result": "Success"
                }
                return Response(data)
            else:
                print("SERIALIZER IS IN VALID")
                data = {
                    "result": "Something went wrong."
                }
                return Response(data)
        else:
            # wallet_address = request.data['wallet']
            # if wallet_address != "None":
            #     print("THE WALLET ADDRESS IS BELOW")
            #     print(wallet_address)
            #     # Load the contract ABI and address
            #     contract_address = config('CONTRACT_ADDRESS')  # Replace with your contract address
            #     contract_abi = contract_abi_const
            #     print("SET THE CONTRACT ADDRRESS AND ABI")

            #     # Create a contract object
            #     contract = w3.eth.contract(address=contract_address, abi=contract_abi)
            #     print("CREATED THE CONTRACT VARIABLE")

            #     # Interact with the contract (e.g., call functions)
            #     result = contract.functions.addWallet(wallet_address, "TEMPORARYADDWALLETPASSCODE").call()
            #     print("RESULT IS BELOW")
            #     print(result)
            #     data = {
            #         "response": "SUCCESS"
            #     }
            #     return Response(data)
            data = {
                    "result": "NOTDEVENVIORNMENT"
                }
            return Response(data)
    except Exception as e:
        print("IN THE EXCEPT BLOCK")
        print(e)
        data = {
            "result": "Something went wrong."
        }
        return Response(data)