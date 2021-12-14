import json

import numpy as np
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render

from sudoker.sudoku import SudokuSolver
from sudoker.search import Search

# Create your views here.
class Solve(APIView):
    def post(self, request):
        request_body = json.loads(request.body)
        data = np.array(request_body["data"])
        # print(data)

        # Solves the puzzle
        solver = Search(SudokuSolver(data))
        solver.search(data)
        solutions = np.array(solver.solutions)
        print("Number of solutions: %s" % (len(solutions)))
        return Response(data={"solutions":solutions}, status=status.HTTP_200_OK)

